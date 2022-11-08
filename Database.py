import Users

#################################################################################################
# Class: Database
# @members: N/A
# @methods: N/A
# 
# This class instantiates the generic database object
#
#################################################################################################

class Database:
    pass

#################################################################################################
# Class: UserDatabase (inherits from Database)
# @members: users
#           numUsers
#
# @methods: AddUser() - Adds a User object to the database
# 
# This class instantiates the User Database. It stores User objects.
#
#################################################################################################


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