from enum import IntEnum

class UserType(IntEnum):
    DEFAULT = 0
    CLIENT = 1
    MANAGER = 2
    SUPPLIER = 3
    ADMIN = 4

class User:
    user_id_counter = 0

    def __init__(self, name: str, pwd: str) -> None:
        self.name = name
        self.password = hash(pwd)
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


class Client(User):
    def __init__(self, name, pwd):
        super().__init__(name, pwd)
        self.manager = None
        self.type = UserType.CLIENT
        self.user_id = f"{self.type.name[0]}" + f"{User.user_id_counter}".zfill(4)
        User.user_id_counter += 1

    def GetManagerID(self):
        if (self.manager == None):
            return None
        return self.manager.GetID()

    def SetManager(self, manager):
        self.manager = manager


class Manager(User):
    def __init__(self, name, pwd):
        super().__init__(name, pwd)
        self.type = UserType.MANAGER
        self.user_id = f"{self.type.name[0]}" + f"{User.user_id_counter}".zfill(4)
        User.user_id_counter += 1

class Supplier(User):
    def __init__(self, name, pwd):
        super().__init__(name, pwd)
        self.type = UserType.SUPPLIER
        self.user_id = f"{self.type.name[0]}" + f"{User.user_id_counter}".zfill(4)
        User.user_id_counter += 1

class Admin(User):
    def __init__(self, name, pwd):
        super().__init__(name, pwd)
        self.type = UserType.ADMIN
        self.user_id = f"{self.type.name[0]}" + f"{User.user_id_counter}".zfill(4)
        User.user_id_counter += 1