import customtkinter as ctk

class GUIData():
    def __init__(self):
        self.active_user_data = {
            "name": ctk.StringVar(),
            "id": ctk.StringVar(),
            "type": ctk.StringVar()
        }
    
        self.users_data = []
    
    def UpdateUserData(self, sys):
        self.users_data = []
        userList = sys.database.get_all_users()
        for user in userList:
            # Get baseline user information
            userID = ctk.StringVar()
            userID.set(value=user[1])
            userName = ctk.StringVar()
            userName.set(value=user[0].replace("_", " "))
            userType = ctk.StringVar()
            userType.set(value=user[2])

            # Assigned manager if type is client
            userManager = ctk.StringVar()
            if (user[2].upper() == "CLIENT"):
                try:
                    manager_id = sys.database.get_manager_from_client(user[1])
                    userManager.set(manager_id)
                except Exception as e:
                    userManager.set("Unassigned")
            else:
                userManager.set("")
            
            userCompany = ctk.StringVar()
            userCompany.set("N/A")
            user_data = [userID, userName, userType, userManager, userCompany]
            self.users_data.append(user_data)