import Users

class Database:
    pass

class UserDatabase(Database):
    def __init__(self) -> None:
        super().__init__()
        self.users = {}
        self.numUsers = 0
    
    def AddUser(self, user: Users.User) -> bool:
        userID = user.GetID()
        self.users[userID] = user
        self.numUsers += 1

    def GetUserByID(self, userID: str) -> Users.User:
        return self.users.get(userID, None)
    
    def GetAllUsers(self) -> list:
        return list(self.users.values())

    def GetNumberOfUsers(self) -> int:
        return self.numUsers