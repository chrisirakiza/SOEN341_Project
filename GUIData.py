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
        self.quotes_data = []
        # self.requests_data_suppliers = []

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
            if (request[5] == 0):
                status.set(value="Waiting for Supplier Response")
            if (request[5] == 1):
                status.set(value="Waiting for Manager Approval")
            if (request[5] == 2):
                status.set(value="Accepted")
            if (request[5] == 3):
                status.set(value="Refused")
            
            # Checks for Quote
            acceptedQuote = ctk.StringVar()
            acceptedQuote.set(value = request[6])
            
            # Add user to users data
            request_data = [requestID,itemName,itemQty,generatedBy,assignedMana,status,acceptedQuote]
            self.requests_data.append(request_data)
    
    def UpdateQuotesManagerData(self, sys) -> None:
        '''Update the list of manager visible quotes data in GUI Data structure'''
        # Reset request data to blank list
        self.quotes_data = []

        # Get list of requests and begin parsing data
        try:
            quoteList = sys.database.get_all_quotes()
        except Exception as e:
            return
        
        for quote in quoteList:
            # Get baseline quote information
            quoteID = ctk.StringVar()
            quoteID.set(value=quote[0])
            reqID = ctk.StringVar()
            reqID.set(value=quote[1])
            price = ctk.StringVar()
            price.set(value=quote[2])
            supplierID = ctk.StringVar()
            supplierID.set(value=quote[3])

            request = sys.database.get_request(reqID)

            #reqID, itemName, quantity, generatedByID, assignedManagerID, status, acceptedQuoteID
            managerID = ctk.StringVar()
            managerID.set(value=request[4])
            itemName = ctk.StringVar()
            itemName.set(value=request[1])
            itemQuantity = ctk.StringVar()
            itemQuantity.set(value=request[2])
            generatedBy = ctk.StringVar()
            generatedBy.set(value=request[3])
            
            # Add user to quote data
            quote_data = [quoteID, reqID, itemName, itemQuantity, price, generatedBy, managerID, supplierID]
            self.quotes_data.append(quote_data)
            