import Users
import Database
import Permissions as perm

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
        self.userDB = Database.UserDatabase() #initialize the user database

        admin_user = Users.Admin('admin', 'admin') #cretes an admin account on system initialization
        self.userDB.AddUser(admin_user)
        self.active_user = admin_user
    
    def SwitchActiveUser(self, userID: str, userPWD: str): #takes a user's ID and password
        user = self.userDB.GetUserByID(userID)
        if (user == None):
            raise Exception(f"User {userID} does not exist in system")
        if (user.GetPassword() != hash(userPWD)):  #verifies if user credentials are correct
            raise Exception(f"Invalid password for user {userID}")
        self.active_user = user    #assigns switched user as active user.
    
    def GetListOfUsers(self) -> str:     #returns list of user's accounts w. names, IDs and user types
        list = ""
        userList = self.userDB.GetAllUsers()
        for user in userList:
            list += f"ID: {user.GetID()}, Name: {user.GetName()}, Type: {user.GetType().name}\n"
        return list
    
    def CreateNewUser(self, type: Users.UserType, name: str, pwd: str) -> str:
        if (type == Users.UserType.ADMIN):
            user = Users.Admin(name, pwd)
        elif (type == Users.UserType.MANAGER):
            user = Users.Manager(name, pwd)
        elif (type == Users.UserType.CLIENT):
            user = Users.Client(name, pwd)
        elif (type == Users.UserType.SUPPLIER):
            user = Users.Supplier(name, pwd)
        else:
            raise Exception(f"Invalid user type")
            return ""
        self.userDB.AddUser(user)
        return user.GetID()

    def CheckPermissions(self, commandType: perm.FunctionTypes) -> bool:    #verifies if a given active user is allowed to execute a given command
         #returns false as default if UserType of active user does not appear in permissions dictionary.
        return perm.Permissions.user_permissions.get(commandType).get(self.active_user.GetType(), False)

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
        
