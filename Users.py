class User:
    user_id_counter = 0

    def __init__(self, name):
        self.name = name
        self.type = type(self).__name__
        self.user_id = f"{self.type[0]}" + f"{User.user_id_counter}".zfill(4)
        User.user_id_counter += 1

    def GetName(self):
        return self.name

    def GetType(self):
        return self.type
    
    def GetID(self):
        return self.user_id


class Client(User):
    pass

class Manager(User):
    pass

class Supplier(User):
    pass

class Admin(User):
    pass