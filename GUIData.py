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

        # Contains all user data and request data, in the format for the user management and request management/review table
        self.users_data = []
        self.requests_data = []

    
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

    def UpdateRequestData(self, sys) -> None:
        '''Update the list of all requests data in GUI Data structure'''
        # Reset request data to blank list
        self.requests_data = []
        # Get list of requests and begin parsing data
        try:
            requestList = sys.database.get_all_requests()
        except Exception as e:
            return
        for request in requestList:
            # Get baseline Request information
            requestID = ctk.StringVar()
            requestID.set(value=request[0])
            itemName = ctk.StringVar()
            itemName.set(value=request[1])
            itemQty = ctk.StringVar()
            itemQty.set(value=request[2])
            generatedBy = ctk.StringVar()
            generatedBy.set(value=request[3])
            assignedMana = ctk.StringVar()
            assignedMana.set(value=request[4])
            # Checks Request Status
            
            status = ctk.StringVar()
            if (request[5] == "0"):
                status.set("Waiting for Supplier response")
            if (request[5] == "1"):
                status.set("Waiting for Manager Approval")
            if (request[5] == "2"):
                status.set("Accepted")
            if (request[5] == "3"):
                status.set("Refused")
            
            # Checks for Quote
            acceptedQuote = ctk.StringVar()
            acceptedQuote.set(value = request[6])
            
            # Add user to users data
            request_data = [requestID,itemName,itemQty,generatedBy,assignedMana,status,acceptedQuote]
            self.requests_data.append(request_data)
            