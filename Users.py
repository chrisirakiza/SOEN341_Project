from enum import IntEnum

#################################################################################################
# Class: UserType
# @members: N/A
# @methods: N/A
# 
# This class instantiates a enumeration for the different UserTypes of the system.
# 
#################################################################################################


class UserType(IntEnum):   
    DEFAULT = 0
    CLIENT = 1
    MANAGER = 2
    SUPPLIER = 3
    ADMIN = 4

    def ParseUserType(userType: str):
        if (userType.lower() == "client"):
            return UserType.CLIENT
        if (userType.lower() == "manager"):
            return UserType.MANAGER
        if (userType.lower() == "supplier"):
            return UserType.SUPPLIER
        if (userType.lower() == "admin"):
            return UserType.ADMIN

#################################################################################################
# Class: Users
# @members: int user_id_counter 
#           str name
#           str password
#           UserType type
#           str user_id
#
# @methods: N/A
# 
# This class generated the general User object. Each User object (and its daughters) contain a name, ID number, password and a UserType.
# When a daughter class object is instatiated, the global user_id_counter is incremented.
#
# 
#################################################################################################

class User:
    user_id_counter = 0

    def __init__(self, name: str, pwd: str) -> None:
        self.name = name
        self.password = hash(pwd)  # hash function for password protection
        self.type = UserType.DEFAULT
        self.user_id = "DEFAULT_ID"

    def GetName(self) -> str:
        return self.name

    def GetType(self) -> UserType:
        return self.type
    
    def GetID(self) -> str:
        return self.user_id
    
    def GetPassword(self) -> str:
        return self.password

#################################################################################################
# Class: Client (inherits from User)
# @members:  Manager manager
#            UserType type
#            str user_id
#
# @methods: SetManager(self, Manager) - Assigns a manager to a client, if the client does not already have one
# 
# This class generates a Client object. The Client is a company employee.
# Each Client has an assigned Manager
# 
#################################################################################################

class Client(User):
    def __init__(self, name, pwd):
        super().__init__(name, pwd)
        self.manager = None
        self.type = UserType.CLIENT
        #User ID consists of the first letter of the User type and a 4 digit number, incremented with each User ID.
        #e.g C0002
        self.user_id = f"{self.type.name[0]}" + f"{User.user_id_counter}".zfill(4) 
        User.user_id_counter += 1

    def GetManagerID(self):
        if (self.manager == None):
            return None
        return self.manager.GetID()

    def SetManager(self, manager):
        self.manager = manager

#################################################################################################
# Class: Manager (inherits from User)
# @members:  UserType type
#            str user_id
#
# @methods: N/A
# 
# This class generates a Manager object. The Manager is a company employee with managerial roles and responsibilities.
# 
# 
#################################################################################################

class Manager(User):
    def __init__(self, name, pwd):
        super().__init__(name, pwd)
        self.type = UserType.MANAGER
        #User ID consists of the first letter of the User type and a 4 digit number, incremented with each User ID.
        #e.g M0001
        self.user_id = f"{self.type.name[0]}" + f"{User.user_id_counter}".zfill(4)
        User.user_id_counter += 1

#################################################################################################
# Class: Supplier (inherits from User)
# @members:  UserType type
#            str user_id
#
# @methods: N/A
# 
# This class generates a Supplier object. The Supplier is an employee from a supplier (external to company).
#
# 
#################################################################################################

class Supplier(User):
    def __init__(self, name, pwd):
        super().__init__(name, pwd)
        self.type = UserType.SUPPLIER
        #User ID consists of the first letter of the User type and a 4 digit number, incremented with each User ID.
        #e.g S0003
        self.user_id = f"{self.type.name[0]}" + f"{User.user_id_counter}".zfill(4)
        User.user_id_counter += 1

#################################################################################################
# Class: Admin (inherits from User)
# @members:  UserType type
#            str user_id
#
# @methods: N/A
# 
# This class generates a Admin object. The Admin is an employee from a company's IT department.
# An Admin can manage data within a database and manager User accounts.
#
# 
#################################################################################################

class Admin(User):
    def __init__(self, name, pwd):
        super().__init__(name, pwd)
        self.type = UserType.ADMIN
        #User ID consists of the first letter of the User type and a 4 digit number, incremented with each User ID.
        #e.g A0000
        self.user_id = f"{self.type.name[0]}" + f"{User.user_id_counter}".zfill(4)
        User.user_id_counter += 1