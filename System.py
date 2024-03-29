import Users
import Database
import Permissions as perm
import Create_Database as db
from RequestForm import ProcurementRequest as request
from RequestForm import RequestStatus as status
import sys

#################################################################################################
# Class: ProcurementSystem
# @members:  userDB
#            User active_user
#            
#
# @methods: SwitchActiveUser() - Changes the current active user of the system.
# .         GetListOfUsers() - Returns a list of all User objects
#           CheckPermissions() - Verifies if a given active user is authorized to execute a given function/command
# 
# This class instantiates the Procurement System. There is only a single instance of the ProcurementSystem, which is
# initialized during system deployement. The ProcurementSystem performs the functional logic of the software. The ProcurementSystem
# also generates the databases required for the software.
#
# 
#################################################################################################

class ProcurementSystem:
    def __init__(self) -> None:
        mysql_password = sys.argv[1]
        self.database = db.Create_Database('localhost', 'root', mysql_password, 'SOEN341')
        self.connection = self.database.connect_to_database()
        #self.userDB = Database.UserDatabase() #initialize the user database
        #admin_user = Users.Admin('admin', 'admin') #cretes an admin account on system initialization
        #self.userDB.AddUser(admin_user)
        self.active_user = 'A0001' #admin_user
    
    def SwitchActiveUser(self, userID: str, userPWD: str): #takes a user's ID and password
        name, userID, pwd, userType = self.GetUserValues(userID)
        #user = self.userDB.GetUserByID(userID)
        # if (user == None):
        #     raise Exception(f"User {userID} does not exist in system")
        if (pwd != userPWD):  #verifies if user credentials are correct
            raise Exception(f"Invalid password for user {userID}")
        self.active_user = userID    #assigns switched user as active user.
        return Users.UserType.ParseUserType(userType)
    
    def GetListOfUsers(self) -> str:     #returns list of user's accounts w. names, IDs and user types
        list = ""
        userList = self.database.get_all_users()
        for user in userList:
            list += f"ID: {user[1]}, Name: {user[0]}, Type: {user[2]}"
            list += "\n"
        return list
    
    def CreateNewUser(self, type: Users.UserType, name: str, pwd: str) -> str:
        user_id_counter = self.database.get_counter_value("USER")
        user_id = f"{type.name[0]}" + f"{user_id_counter + 1}".zfill(4)
        userType = type.name
        self.database.add_user(name, user_id, pwd, userType)
        return user_id

    #name, userID, pwd, userType
    def GetUserValues(self, userID: str):
        name, userID, pwd, userType = self.database.get_user(userID)
        return name, userID, pwd, userType
        

    def CheckPermissions(self, commandType: perm.FunctionTypes) -> bool:    #verifies if a given active user is allowed to execute a given command
         #returns false as default if UserType of active user does not appear in permissions dictionary.
        name, userID, pwd, userType = self.database.get_user(self.active_user)
        type = Users.UserType.ParseUserType(userType)
        return perm.Permissions.user_permissions.get(commandType).get(type, False)

    def AssignManager(self, clientID: str, managerID: str):
        c_name, c_userID, c_pwd, c_userType = self.database.get_user(clientID)
        m_name, m_userID, m_pwd, m_userType = self.database.get_user(managerID)

        if (Users.UserType.ParseUserType(c_userType) != Users.UserType.CLIENT):
            raise Exception(f"Passed client ID is not user of type client")
        if (Users.UserType.ParseUserType(m_userType) != Users.UserType.MANAGER):
            raise Exception(f"Passed manager ID is not user of type manager")

        self.database.assign_manager_to_client(c_userID, m_userID)
    
    #create Procurement Request
    def CreateRequest(self,client_id, item, quantity):
        request_counter = self.database.get_counter_value("PROCUREMENT_REQUEST")
        reqNum = f"R" + f"{request_counter + 1}".zfill(6)
        stat = status.SENT_TO_SUPPLIER
        managerID = self.database.get_manager_from_client(client_id)
        self.database.add_procurement_request(reqNum, item, quantity, client_id, managerID, stat)
        return reqNum
        
    #access the database to get request status
    def displayStatus(self,request_id):
        return self.database.get_request_status(request_id)

    #display all procurement request info given request ID

    def displayRequest(self,request_id):
        return self.database.get_procurement_request(request_id)

    def ResetPassword(self,user_id,new_pw):
        u_ID = self.database.get_user(user_id)[1]
        self.database.assign_new_password(u_ID,new_pw)
        
    def supplier_functionality(self):
        if(Users.UserType.ParseUserType(self.active_user) != Users.UserType.SUPPLIER):
            supplier_requests = self.database.get_supplier_requests(self.active_user)
            print("Request Number", "Item Name", "Quantity", "Generated By", "Assigned Manager")
            temp = [[supplier_requests[i][1], supplier_requests[i][2], supplier_requests[i][3], supplier_requests[i][4], supplier_requests[i][5]] for i in supplier_requests]
            print(temp)
    
    # supplier defines the quote for a given request
    def CreateQuote(self,Price , requestNumber):
        # Create quote ID ( use the same as userID logic)
        quote_id_counter = self.database.get_counter_value("QUOTE")
        quote_id = f"Q" + f"{quote_id_counter + 1}".zfill(4)

        # fetch the item name and quantity to give it a price
        # if the request number matches then get item name and quantity. 
        item_name, quantity = self.database.get_item(self.active_user, requestNumber)
        self.database.add_new_quote(self, quote_id, requestNumber, Price, self.active_user)
        requestID = self.database.get_request_id_from_quote(quote_id)
        #set the status of the request to "send to manager"
        self.database.edit_request_status(requestID, status.SENT_TO_MANAGER) 
        #check if the price is less than 5000, auto-approve if it is 
        if (Price<5000.00):
            self.AutoAcceptQuote(quote_id)

    #automatically accept a quote by setting the status to "auto accepted", add the quoteID to the approvedQuoteID
    #and delete all other quotes for the given request
    def AutoAcceptQuote(self, quote_id):
        requestID = self.database.get_request_id_from_quote(quote_id)
        self.database.edit_request_status(requestID, status.AUTOMATICALLY_APPROVED)
        self.database.quote_approved(quote_id,requestID)
        self.database.delete_all_other_quotes(requestID,quote_id)


    #given the quoteID, accept a procurement request, deleting all other quotes for the request
    def ManagerAcceptQuote(self,quote_id):
        requestID = self.database.get_request_id_from_quote(quote_id)
        self.database.edit_request_status(requestID, status.APPROVED_BY_MANAGER)
        self.database.quote_approved(quote_id,requestID)
        self.database.delete_all_other_quotes(requestID,quote_id)
    
    #given the requestID, delete all the quotes associated with it and set the status to "denied"
    def ManagerDenyRequest(self,request_id):
        self.database.edit_request_status(request_id, status.DENIED_BY_MANAGER)
        self.database.delete_all_quotes(request_id)
