import Users

class ProcurementSystem:
    def __init__(self):
        self.user_list = []
        self.number_of_users = 0
        admin_user = Users.Admin('Admin')
        self.AddUser(admin_user)
        self.active_user = admin_user
    
    def AddUser(self, user):
        self.user_list.append(user)
        self.number_of_users += 1
        return True
    
    def SwitchActiveUser(self, name):
        for user in self.user_list:
            if user.name == name:
                self.active_user = user
                return True
        return False
    
    def GetListOfUsers(self):
        list = ""
        for user in self.user_list:
            list += f"ID: {user.GetID()}, Name: {user.GetName()}, Type: {user.GetType()}\n"
        return list
    
