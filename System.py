import Users
import Database
import Permissions as perm

class ProcurementSystem:
    def __init__(self) -> None:
        self.userDB = Database.UserDatabase()

        admin_user = Users.Admin('admin', 'admin')
        self.userDB.AddUser(admin_user)
        self.active_user = admin_user
    
    def SwitchActiveUser(self, userID: str, userPWD: str) -> bool:
        user = self.userDB.GetUserByID(userID)
        if (user == None):
            return False
        if (user.GetPassword() != hash(userPWD)):
            return False
        self.active_user = user
        return True
    
    def GetListOfUsers(self) -> str:
        list = ""
        userList = self.userDB.GetAllUsers()
        for user in userList:
            list += f"ID: {user.GetID()}, Name: {user.GetName()}, Type: {user.GetType().name}\n"
        return list
    
    def CheckPermissions(self, commandType: perm.FunctionTypes) -> bool:
        return perm.Permissions.user_permissions.get(commandType).get(self.active_user.GetType(), False)