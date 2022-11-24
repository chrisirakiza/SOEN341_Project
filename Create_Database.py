import mysql.connector
from mysql.connector import Error

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

    def add_user(self, name, user_id, password, user_type):
        query_add_user = """ INSERT INTO USER VALUES (default, '%s', '%s', '%s', '%s')"""%(name, user_id, password, user_type)    
        self.execute_query(connection, query_add_user)
    
    def assign_manager_to_client(self, clientID: str, managerID: str):
        self.execute_query(connection, """INSERT INTO MANAGER VALUES ('%s', '%s')""" %(clientID, managerID))

    def add_procurement_request(self, rnum, item, quantity, client_id, manager_id, status):
        query_add_request = """INSERT INTO PROCUREMENT_REQUEST VALUES (default, '%s', '%s', %d, '%s', '%s', %d, default)""" %(rnum, item, int(quantity), client_id, manager_id, status.value)
        self.execute_query(connection, query_add_request)


    def get_manager_from_client(self, clientID: str):
        query_get_manager = """SELECT managedBy FROM MANAGER WHERE MANAGER.clientID = '%s'""" %(clientID)
        managerID = self.read_query(connection, query_get_manager)
        if managerID == []:
            raise Exception(f"User {clientID} does not have an assigned manager")
        return managerID[0][0]


    def get_supplier_requests(self, supplier_ID):
        get_item = """ SELECT productType FROM COMPANY WHERE COMPANY.supplierID = "%s" """%(supplier_ID)
        get_requests = """SELECT * FROM PROCUREMENT_REQUEST WHERE PROCUREMENT_REQUEST.itemName = "%s" """%(get_item[0][0])
        return get_requests


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
                                            status INTEGER,
                                            acceptedQuoteID VARCHAR(10) DEFAULT(NULL),
                                            INDEX(id)
                                            )"""
    
    create_table_quote =               """CREATE TABLE QUOTE(
                                            id INTEGER NOT NULL UNIQUE AUTO_INCREMENT, 
                                            quoteID VARCHAR(10) PRIMARY KEY NOT NULL,
                                            requestID VARCHAR(20),
                                            price FLOAT(7, 2),
                                            supplierName VARCHAR(100) REFERENCES USER(name),
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

    

DB = Create_Database('localhost', 'root', "star26", "SOEN341")
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
