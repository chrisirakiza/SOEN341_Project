class User:
    def __init__(self, name):
        self.name = name
        self.type = 'User'

class Client(User):
    def __init__(self, name):
        super().__init__(name)
        self.type = 'Client'

class Manager(User):
    def __init__(self, name):
        super().__init__(name)
        self.type = 'Manager'

class Supplier(User):
    def __init__(self, name):
        super().__init__(name)
        self.type = 'Supplier'

class Admin(User):
    def __init__(self, name):
        super().__init__(name)
        self.type = 'Admin'