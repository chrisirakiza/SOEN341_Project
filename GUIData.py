import customtkinter as ctk

class GUIData():
    '''Contains GUI data for use in tkinter textvariables'''
    def __init__(self) -> None:
        # Contains the active user data
        self.active_user_data = {
            "name": ctk.StringVar(),
            "id": ctk.StringVar(),
            "type": ctk.StringVar()
        }

        # Contains all user data, in the format for the user management table
        self.users_data = []
    
    def UpdateUserData(self, sys) -> None:
        '''Update the list of all user data in GUI Data structure'''
        # Reset users data to blank list
        self.users_data = []
        # Get list of users and begin parsing data
        try:
            userList = sys.database.get_all_users()
        except Exception as e:
            return
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
            
            # Assign company to supplier
            userCompany = ctk.StringVar()
            if (user[2].upper() == "SUPPLIER"):
                userCompany.set("Unassigned")
            else:
                userCompany.set("")
            
            # Add user to users data
            user_data = [userID, userName, userType, userManager, userCompany]
            self.users_data.append(user_data)