import Users
import Database

class ProcurementSystem:
    def __init__(self) -> None:
        self.userDB = Database.UserDatabase()

        admin_user = Users.Admin('Admin')
        self.userDB.AddUser(admin_user)
        self.active_user = admin_user
    
    def SwitchActiveUser(self, userID: str) -> bool:
        user = self.userDB.GetUserByID(userID)
        if (user == None):
            return False
        self.active_user = user
        return True
    
    def GetListOfUsers(self) -> str:
        list = ""
        userList = self.userDB.GetAllUsers()
        for user in userList:
            list += f"ID: {user.GetID()}, Name: {user.GetName()}, Type: {user.GetType()}\n"
        return list
    