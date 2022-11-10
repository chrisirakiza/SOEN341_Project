import mysql.connector
from mysql.connector import Error

class design_database:
            
    host, user, pwd, dbName = '', '', '', ''
    def __init__(self, host, user, password, dbName):
        self.host = host
        self.user = user
        self.pwd = password
        self.dbName = dbName
        
    #EXECUTE A QUERY
        
    def execute_query(self, connection, mysql_query):
        cursor = connection.cursor()
        try:
            cursor.execute(mysql_query)
            connection.commit()
            print("Query successful")
        except Error as e:
            print("Error: ", e)
            
    #READ DATA FROM DATABASE
                        
    def read_query(self, connection, mysql_query):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(mysql_query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print("Error: ", e)

    #CONNECT TO THE MYSQL DATABASE
            
    def connect_to_database(self):
        connection = None
        try:
            connection = mysql.connector.connect(host = self.host, user = self.user, passwd = self.pwd)
            print("Connected to Server: Admin")
            existing_db = self.read_query(connection, "SHOW DATABASES")
            if ('soen341',) not in existing_db:
                self.execute_query(connection, "CREATE DATABASE SOEN341")
                print("Created Database: ", self.dbName)

            connection = mysql.connector.connect(host = self.host, user = self.user, passwd = self.pwd, database = self.dbName)
            print("Connected to Database: ", self.dbName)
        except Error as e:
            print("Error: ", e)

        return connection

    #DESIGNING QUERIES TO BUILD DATABASE

    create_table_user =                """CREATE TABLE USER(
                                            id INTEGER NOT NULL AUTO_INCREMENT,
                                            name VARCHAR(100),
                                            userID VARCHAR(10) PRIMARY KEY NOT NULL,
                                            password VARCHAR(20),
                                            userType VARCHAR(50),
                                            INDEX(id))"""
   
    create_table_procurement_request = """CREATE TABLE PROCUREMENT_REQUEST(
                                            id INTEGER NOT NULL AUTO_INCREMENT,
                                            requestNumber VARCHAR(20) PRIMARY KEY NOT NULL,
                                            itemName VARCHAR(200),
                                            generatedBy VARCHAR(100) REFERENCES USER(name),
                                            assignedManager VARCHAR(100) REFERENCES USER(name),
                                            status BOOLEAN DEFAULT(0),
                                            acceptedQuoteID VARCHAR(10),
                                            INDEX(id)
                                            )"""
    
    create_table_quote =               """CREATE TABLE QUOTE(
                                            id INTEGER NOT NULL AUTO_INCREMENT, 
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
    


DB = design_database('localhost', 'root', '#Snroshan1998', "soen341")
connection = DB.connect_to_database()

DB.execute_query(connection, DB.create_table_user)
DB.execute_query(connection, DB.create_table_procurement_request)
DB.execute_query(connection, DB.create_table_quote)
DB.execute_query(connection, DB.create_table_company)


# DB2 = design_database('localhost', 'root', '#Snroshan1998', "soen341")
# connection = DB2.connect_to_database()

# def add_user(name, user_id, password, user_type):
#     query_add_user = """ INSERT INTO USER VALUES (default, '%s', '%s', '%s', '%s')"""%(name, user_id, password, user_type)    
#     DB2.execute_query(connection, query_add_user)
    
# def get_user(user_id):
#     query_get_user = """SELECT * FROM USER WHERE USER.userID = "%s" """ %(user_id)
#     user_data = DB2.read_query(connection, query_get_user)
#     return user_data[0][1], user_data[0][2], user_data[0][3], user_data[0][4]

# def get_counter_value():
#     query_get_last_count = """SELECT MAX(id) FROM USER"""
#     counter = DB2.read_query(connection, query_get_last_count)
#     return int(counter[0][0])

# add_user('Rosh', 'A0001', 'bleh', 'Admin')
# print(get_user('A0000'))
# get_counter_value()