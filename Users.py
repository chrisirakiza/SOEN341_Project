class User:
    user_id_counter = 0

    def __init__(self, name: str) -> None:
        self.name = name
        self.type = type(self).__name__
        self.user_id = f"{self.type[0]}" + f"{User.user_id_counter}".zfill(4)
        User.user_id_counter += 1

    def GetName(self) -> str:
        return self.name

    def GetType(self) -> str:
        return self.type
    
    def GetID(self) -> str:
        return self.user_id


class Client(User):
    def __init__(self, name):
        super().__init__(name)
        self.manager = None

    def GetManagerID(self):
        if (self.manager == None):
            return None
        return self.manager.GetID()

    def SetManager(self, manager):
        self.manager = manager


class Manager(User):
    pass

class Supplier(User):
    pass

class Admin(User):
    pass