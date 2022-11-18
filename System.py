import Users
import Database
import Permissions as perm
import Create_Database as db
from RequestForm import ProcurementRequest as request
from RequestForm import RequestStatus as status

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
        self.database = db.Create_Database('localhost', 'root', "star26", 'SOEN341')
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
        reqNum = f"22" + f"{request_counter + 1}".zfill(6)
        stat = status.SENT_TO_SUPPLIER
        managerID = self.database.get_manager_from_client(client_id)
        self.database.add_procurement_request(reqNum, item, quantity, client_id, managerID, stat)
        return reqNum

    def ResetPassword(self,user_id,new_pw):
        u_ID = self.database.get_user(user_id)[1]
        self.database.assign_new_password(u_ID,new_pw)
        
        

        
