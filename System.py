import Users
import Database
import Permissions as perm
import Create_Database as db

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
        self.database = db.Create_Database('localhost', 'root', 'star26', 'SOEN341')
        self.connection = self.database.connect_to_database()
        
        
        self.userDB = Database.UserDatabase() #initialize the user database

        

        admin_user = Users.Admin('admin', 'admin') #cretes an admin account on system initialization
        self.userDB.AddUser(admin_user)
        self.active_user = 'A0001' #admin_user
    
    def SwitchActiveUser(self, userID: str, userPWD: str): #takes a user's ID and password
        name, userID, pwd, userType = self.GetUserValues(userID)
        #user = self.userDB.GetUserByID(userID)
        # if (user == None):
        #     raise Exception(f"User {userID} does not exist in system")
        if (pwd != userPWD):  #verifies if user credentials are correct
            raise Exception(f"Invalid password for user {userID}")
        self.active_user = userID    #assigns switched user as active user.
        return userType
    
    def GetListOfUsers(self) -> str:     #returns list of user's accounts w. names, IDs and user types
        list = ""
        print(self.database.get_all_users())
        userList = self.database.get_all_users()
        print(userList)
        for user in userList:
            print(user)
            list += f"ID: {user[1]}, Name: {user[0]}, Type: {user[2]}\n"
        # userList = self.userDB.GetAllUsers()
        # for user in userList:
        #     list += f"ID: {user.GetID()}, Name: {user.GetName()}, Type: {user.GetType().name}\n"
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
        client = self.userDB.GetUserByID(clientID)
        manager = self.userDB.GetUserByID(managerID)
        if (client == None):
            raise Exception(f"Client does not exist in the system")
        if (manager == None):
            raise Exception(f"Manager does not exist in the system")
        if (client.GetType() != Users.UserType.CLIENT):
            raise Exception(f"Passed client ID is not user of type client")
        if (manager.GetType() != Users.UserType.MANAGER):
            raise Exception(f"Passed manager ID is not user of type manager")
        client.SetManager(manager)
        
