import mysql.connector
from mysql.connector import Error
import sys

class Create_Database:
            
    host, user, pwd, dbName = '', '', '', ''
    def __init__(self, host, user, password, dbName):
        self.host = host
        self.user = user
        self.pwd = password
        self.dbName = dbName
        
    #EXECUTE A QUERY

    def execute_query(self, connection, mysql_query, verbose = False):
        cursor = connection.cursor()
        try:
            cursor.execute(mysql_query)
            connection.commit()
            if (verbose):
                print("Query successful")
        except Error as e:
            if (verbose):
                print("Error: ", e)
            
    #READ DATA FROM DATABASE
                        
    def read_query(self, connection, mysql_query, verbose = False):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(mysql_query)
            result = cursor.fetchall()
            return result
        except Error as e:
            if (verbose):
                print("Error: ", e)

    #CONNECT TO THE MYSQL DATABASE
            
    def connect_to_database(self):
        connection = None
        try:
            connection = mysql.connector.connect(host = self.host, user = self.user, passwd = self.pwd)
            print("Connected to Server: Admin")
            existing_db = self.read_query(connection, "SHOW DATABASES")
            if ('SOEN341',) not in existing_db:
                self.execute_query(connection, "CREATE DATABASE SOEN341")
                print("Created Database: ", self.dbName)

            connection = mysql.connector.connect(host = self.host, user = self.user, passwd = self.pwd, database = self.dbName)
            print("Connected to Database: ", self.dbName)
        except Error as e:
            print("Error: ", e)

        return connection
    
    def check_admin(self):
        if (self.read_query(connection, """SELECT * FROM USER WHERE userID = 'A0001' """) == []): 
            self.execute_query(connection, """INSERT INTO USER VALUES(0, 'admin', 'A0001', 'admin', 'ADMIN')""")

    def get_counter_value(self, counterType: str):
        query_get_last_count = """SELECT MAX(%s.id) FROM %s"""%(counterType, counterType)
        counter = self.read_query(connection, query_get_last_count)
        if (counter == []):
            raise Exception(f"Unexpected counterType passed")
        if (counter[0][0] == None):
            return 0
        return int(counter[0][0])

    def get_all_users(self):
        query_users = """SELECT * FROM USER"""
        user_data = self.read_query(connection, query_users)
        if user_data == []:
            raise Exception(f"No users present in database")
        return [[i[1], i[2], i[4]] for i in user_data]

    def get_user(self, user_id: str):
        query_get_user = """SELECT * FROM USER WHERE USER.userID = "%s" """ %(user_id)
        user_data = self.read_query(connection, query_get_user)
        if user_data == []:
            raise Exception(f"User ({user_id}) not found in database")
        return user_data[0][1], user_data[0][2], user_data[0][3], user_data[0][4]

    def get_request(self, reqID: str):
        '''Returns: reqID, itemName, quantity, generatedByID, assignedManagerID, status, acceptedQuoteID'''
        query_get_request = """SELECT * FROM PROCUREMENT_REQUEST WHERE PROCUREMENT_REQUEST.requestNumber = "%s" """ %(reqID)
        request_data = self.read_query(connection, query_get_request)
        if request_data == []:
            raise Exception(f"Request ({reqID}) not found in database")
        #reqID, itemName, quantity, generatedByID, assignedManagerID, status, acceptedQuoteID
        return request_data[0][1], request_data[0][2], request_data[0][3], request_data[0][4], request_data[0][5], request_data[0][6], request_data[0][7]

    def get_all_requests(self):
        query_get_request = """SELECT * FROM PROCUREMENT_REQUEST"""
        request_data = self.read_query(connection, query_get_request)
        if request_data == []:
            raise Exception(f"No Requests found in database")
        return [[i[1], i[2], i[3], i[4], i[5], i[6], i[7]] for i in request_data]

    def add_user(self, name, user_id, password, user_type):
        query_add_user = """ INSERT INTO USER VALUES (default, '%s', '%s', '%s', '%s')"""%(name, user_id, password, user_type)    
        self.execute_query(connection, query_add_user)
    
    def assign_manager_to_client(self, clientID: str, managerID: str):
        assign_manager_query = """INSERT INTO MANAGER VALUES ('%s', '%s')""" %(clientID, managerID)
        self.execute_query(connection,assign_manager_query)

    #add a new procurement request to the database 
    def add_procurement_request(self, rnum, item, quantity, client_id, manager_id, status):
        query_add_request = """INSERT INTO PROCUREMENT_REQUEST VALUES (default, '%s', '%s', %d, '%s', '%s', %d, default)""" %(rnum, item, int(quantity), client_id, manager_id, status.value)
        self.execute_query(connection, query_add_request)

    def assign_new_password(self,user_ID,new_pw):
        query_update_request = """UPDATE USER SET password = '%s' WHERE userID = '%s'""" %(new_pw,user_ID)
        self.execute_query(connection, query_update_request)
    # given a userID (of a worker at the company), return the worker's ManagerID
    def get_manager_from_client(self, clientID: str):
        query_get_manager = """SELECT managedBy FROM MANAGER WHERE MANAGER.clientID = '%s'""" %(clientID)
        managerID = self.read_query(connection, query_get_manager)
        if managerID == []:
            raise Exception(f"User {clientID} does not have an assigned manager")
        return managerID[0][0]
    #query the database for a procurement request given its ID
    def get_procurement_request(self, procurement_id: int):
        query_get_request = """SELECT * FROM PROCUREMENT_REQUEST WHERE PROCUREMENT_REQUEST.requestNumber = "%s" """ %(procurement_id)
        request_data = self.read_query(connection, query_get_request)
        if request_data == []:
            raise Exception(f"Request ({procurement_id}) not found in database")
        return request_data[0][1], request_data[0][2], request_data[0][3], request_data[0][4], request_data[0][5], request_data[0][6], request_data[0][7]
    #query the database for the status of a procurement request given its ID
    def get_request_status(self, procurement_id:int):
        request_data = self.get_procurement_request(procurement_id)
        if request_data == []:
            raise Exception(f"Request ({procurement_id}) not found in database")
        return request_data[0][6]
        
    def get_supplier_requests(self, supplier_ID):
        get_item_query = """ SELECT productType FROM COMPANY WHERE COMPANY.supplierID = "%s" """%(supplier_ID)
        get_item = self.read_query(connection, get_item_query)
        get_requests_query = """SELECT * FROM PROCUREMENT_REQUEST WHERE PROCUREMENT_REQUEST.itemName = "%s" """%(get_item[0][0])
        get_requests = self.read_query(connection, get_requests_query)
        return get_requests
    
    def get_item(self, supplier_ID, requestNUM):
        get_item_query = """ SELECT productType FROM COMPANY WHERE COMPANY.supplierID = "%s" """%(supplier_ID)
        get_item = self.read_query(connection, get_item_query)
        get_requests_query = """SELECT itemName, quantity FROM PROCUREMENT_REQUEST WHERE PROCUREMENT_REQUEST.requestNumber = "%s" AND PROCUREMENT_REQUEST.itemName = "%s" """%(requestNUM, get_item[0][0])
        get_requests = self.read_query(connection, get_requests_query)
        if get_requests == []:
            raise Exception (f"Item ({requestNUM}) not found in database")
        return get_requests[0][0], get_requests[0][1]
    
    #add a new quote to the database
    def add_new_quote(self, quote_id, request_number, price, supplier_id):
        query_add_quote = """ INSERT INTO QUOTE VALUES (default, "%s", "%s", %f, "%s") """ %(quote_id, request_number, price, supplier_id)
        self.execute_query(connection, query_add_quote)

    #given a quoteID, return the requestID associated with it
    def get_request_id_from_quote(self, quote_id):
        get_quote_query = """SELECT * FROM QUOTE WHERE QUOTE.quoteID = "%s" """%(quote_id)
        quote_data = self.read_query(connection, get_quote_query)
        if quote_data == []:
            raise Exception (f"Error: quote ({quote_id}) does not exist in database")
        request_id = quote_data[0][2]
        return request_id

    #set the status of a request (sent to supplier,auto approved,sent to manager, approved by manager, denied by manager)
    def edit_request_status(self, request_id,status):
        get_request_query = """SELECT * FROM QUOTE WHERE QUOTE.requestID = '%s'"""%(request_id) #"UPDATE USER SET password = '%s' WHERE userID = '%s'" %(new_pw,user_ID)
        request = self.read_query(connection,get_request_query)
        if request == []:
            raise Exception (f"Error: request ({request_id}) does not exist in database")
        # query_update_request = """UPDATE USER SET password = '%s' WHERE userID = '%s'""" %(new_pw,user_ID)
        edit_request_status_query = """UPDATE PROCUREMENT_REQUEST SET status = '%s' WHERE requestNumber = '%s'"""%(str(status),request_id)
        self.execute_query(connection, edit_request_status_query)
    #return all quotes in the database
    def get_all_quotes(self):
        query_get_quotes = """SELECT * FROM QUOTE"""
        quote_data = self.read_query(connection, query_get_quotes)
        return [[i[1], i[2], i[3], i[4]] for i in quote_data]
        # Quoteid , reqid, price, supplierid
    #adds the quoteID to the acceptedQuoteID value in the procurementRequest table in the database
    def quote_approved(self,quote_id,request_id):
        get_quote_query = """SELECT * FROM QUOTE WHERE QUOTE.quoteID = '%s'"""%(quote_id)
        quote = self.read_query(connection,get_quote_query)
        if quote == []:
            raise Exception (f"Error: quote ({quote_id}) does not exist in database")
        approve_quote_query = """UPDATE PROCUREMENT_REQUEST SET acceptedQuoteID = '%s' WHERE requestNumber = '%s' """%(quote_id, request_id)
        self.execute_query(connection,approve_quote_query)
    #delete all quotes from a certain request
    def delete_all_quotes(self,request_id):
        delete_quote_query = """DELETE FROM QUOTE WHERE QUOTE.requestID = '%s'"""%(request_id)
        self.execute_query(connection,delete_quote_query)

        
    #delete all quotes except the one that's been approved
    def delete_all_other_quotes(self,quote_id,request_id):
        get_quote_table = """SELECT * FROM QUOTE WHERE QUOTE.requestID = '%s'"""%(request_id)
        get_quote = self.read_query(connection,get_quote_table)
        for i,quote in enumerate(get_quote):
            if (get_quote[i][1]!=quote_id):
                delete_quote_query = """DELETE FROM QUOTE WHERE QUOTE.quoteID ='%s'"""%(get_quote[i][1])
                self.execute_query(connection,delete_quote_query)

    def add_company(self,companyName):
        get_company_query = """SELECT * FROM COMPANY WHERE COMPANY.companyName = '%s'"""%(companyName)
        get_company = self.read_query(connection,get_company_query)
        if(get_company != []):
            raise Exception (f"{companyName} already exists in database")
        add_company_query = """INSERT INTO COMPANY (companyName) VALUES ('%s');"""%(companyName)
        self.execute_query(connection, add_company_query)

    def get_company_from_name(self,companyName):
        get_company_query = """SELECT * FROM COMPANY WHERE COMPANY.companyName = '%s'"""%(companyName)
        get_company = self.read_query(connection,get_company_query)
        if(get_company == []):
            raise Exception (f"{companyName} does not exist in database")
        return get_company

    def get_supplier_requests(self, supplier_ID):
        get_item_query = """ SELECT productType FROM COMPANY WHERE COMPANY.supplierID = "%s" """%(supplier_ID)
        get_item = self.read_query(connection, get_item_query)
        get_requests_query = """SELECT * FROM PROCUREMENT_REQUEST WHERE PROCUREMENT_REQUEST.itemName = "%s" """%(get_item[0][0])
        get_requests = self.read_query(connection, get_requests_query)
        return get_requests
    
    def get_item(self, supplier_ID, requestNUM):
        get_item_query = """ SELECT productType FROM COMPANY WHERE COMPANY.supplierID = "%s" """%(supplier_ID)
        get_item = self.read_query(connection, get_item_query)
        get_requests_query = """SELECT itemName, quantity FROM PROCUREMENT_REQUEST WHERE PROCUREMENT_REQUEST.requestNumber = "%s" AND PROCUREMENT_REQUEST.itemName = "%s" """%(requestNUM, get_item[0][0])
        get_requests = self.read_query(connection, get_requests_query)
        return get_requests[0][0], get_requests[0][1]
    
    def add_item(self,companyName,companyItems):
        add_item_query = """UPDATE COMPANY SET productType = ('%s') WHERE companyName = '%s'"""%(companyItems,companyName)
        self.execute_query(connection,add_item_query)

    def add_new_quote(self, quote_id, request_number, price, supplier_id):
        query_add_quote = """ INSERT INTO QUOTE VALUES (default, "%s", "%s", %f, "%s") """ %(quote_id, request_number, price, supplier_id)
        self.execute_query(connection, query_add_quote)
    
    # finding the suppliers that provide the item you are looking for            
    def get_suppliers(itemName):
        query_get_supplier = """ SELECT supplierID FROM COMPANY WHERE %s = COMPANY.productType """ %(itemName)
        supplier_data = DB.read_query(connection, query_get_supplier)
        return  [[i[1]] for i in supplier_data]
    
    def get_company_data(self):
        query_get_company = """ SELECT * FROM COMPANY """
        company_data = DB.read_query(connection, query_get_company)
        return [[i[3],i[4]] for i in company_data]

# compare quotes from suppliers and take the lowest offering 
    def compare_quote():
        query_compare_quote = """ SELECT * FROM QUOTE ORDER BY QUOTE.price ASC """ 
        compare_quote_data = DB.read_query(connection, query_compare_quote)
        return compare_quote_data[0][1], compare_quote_data[1][1]
        
        
    #DESIGNING QUERIES TO BUILD DATABASE

    create_table_user =                """CREATE TABLE USER(
                                            id INTEGER NOT NULL UNIQUE AUTO_INCREMENT,
                                            name VARCHAR(100),
                                            userID VARCHAR(10) PRIMARY KEY NOT NULL,
                                            password VARCHAR(20),
                                            userType VARCHAR(50),
                                            INDEX(id))"""
   
    create_table_procurement_request = """CREATE TABLE PROCUREMENT_REQUEST(
                                            id INTEGER NOT NULL UNIQUE AUTO_INCREMENT,
                                            requestNumber VARCHAR(20) PRIMARY KEY NOT NULL,
                                            itemName VARCHAR(200),
                                            quantity INTEGER,
                                            generatedBy VARCHAR(10) REFERENCES USER(userID),
                                            assignedManager VARCHAR(10) REFERENCES USER(userID),
                                            status VARCHAR(200),
                                            acceptedQuoteID VARCHAR(10) DEFAULT(NULL),
                                            INDEX(id)
                                            )"""
    
    create_table_quote =               """CREATE TABLE QUOTE(
                                            id INTEGER NOT NULL UNIQUE AUTO_INCREMENT, 
                                            quoteID VARCHAR(10) PRIMARY KEY NOT NULL,
                                            requestID VARCHAR(20),
                                            price FLOAT(9, 2),
                                            supplierID VARCHAR(10) REFERENCES USER(userID),
                                            INDEX(id),
                                            FOREIGN KEY (requestID) REFERENCES PROCUREMENT_REQUEST(requestNumber)
                                            ON DELETE CASCADE)"""

    create_table_company =             """CREATE TABLE COMPANY(   
                                            ID INTEGER PRIMARY KEY AUTO_INCREMENT,
                                            supplierID VARCHAR(10),
                                            supplierName VARCHAR(100) REFERENCES USER(name),
                                            companyName VARCHAR(200),
                                            productType VARCHAR(100),
                                            contactInfo VARCHAR(200),
                                            FOREIGN KEY (supplierID) REFERENCES USER(userID)
                                            ON UPDATE CASCADE ON DELETE CASCADE
                                            )"""
                                            
    create_table_manager =              """CREATE TABLE MANAGER (
                                            clientID VARCHAR(10) UNIQUE NOT NULL,
                                            managedBy VARCHAR(10) REFERENCES USER(userID),

                                            FOREIGN KEY (clientID) REFERENCES USER(userID)
                                            ON DELETE CASCADE
                                            )"""


mysql_password = sys.argv[1]
DB = Create_Database('localhost', 'root', mysql_password, "SOEN341")
connection = DB.connect_to_database()

DB.execute_query(connection, DB.create_table_user)
DB.execute_query(connection, DB.create_table_procurement_request)
DB.execute_query(connection, DB.create_table_quote)
DB.execute_query(connection, DB.create_table_company)
DB.execute_query(connection, DB.create_table_manager)
DB.check_admin()

# TO IMPLEMENT:
#query_add_request = """INSERT INTO PROCUREMENT_REQUEST VALUES (default, '%s', '%s', %d, '%s', '%s', %d))""" %(rnum, itemName, quantity, generatedBy, assignedManager, status)
#Create_Database.execute_query(connection, query_add_request)
