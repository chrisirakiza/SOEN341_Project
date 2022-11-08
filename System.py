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
    
    def SwitchActiveUser(self, userID: str, userPWD: str) -> bool: #takes a user's ID and password
        user = self.userDB.GetUserByID(userID)
        if (user == None):
            return False
        if (user.GetPassword() != hash(userPWD)):  #verifies if user credentials are correct
            return False
        self.active_user = user    #assigns switched user as active user.
        return True
    
    def GetListOfUsers(self) -> str:     #returns list of user's accounts w. names, IDs and user types
        list = ""
        userList = self.userDB.GetAllUsers()
        for user in userList:
            list += f"ID: {user.GetID()}, Name: {user.GetName()}, Type: {user.GetType().name}\n"
        return list
    
    def CheckPermissions(self, commandType: perm.FunctionTypes) -> bool:    #verifies if a given active user is allowed to execute a given command
         #returns false as default if UserType of active user does not appear in permissions dictionary.
        return perm.Permissions.user_permissions.get(commandType).get(self.active_user.GetType(), False)

    def AssignManager(self, client: Users.Client, manager: Users.Manager) -> bool:
         #to be implented
            return True
