import customtkinter as ctk # pip install customtkinter
import GUIData
import GUIFrames
import System
import Users
import PopUp as pu
from Permissions import FunctionTypes as perm

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

class ProcSysGUI(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.sys = System.ProcurementSystem()
        self.gui_data = GUIData.GUIData()
        self.gui_data.UpdateUserData(self.sys)
        self.gui_data.UpdateRequestData(self.sys)
        self.gui_data.UpdateQuotesManagerData(self.sys)
        self.gui_data.UpdateRequestDataSuppliers(self.sys)

        self.UpdateActiveUser()

        self.title("Procurement System Prototype")
        self.geometry("800x600")
        # Configure main window so it has a navigation bar and a main screen
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Generate navigation bar
        self.nav_bar = GUIFrames.NavBar(root=self, master=self, width=180, corner_radius=0)
        self.nav_bar.grid(row=0, column=0, sticky="nswe")

        # Generate all possible pages

        self.pageDict = {}
        self.pageDict[GUIFrames.PageTypes.PLACEHOLDER] = GUIFrames.PlaceHolderPage(root=self, master=self)
        self.pageDict[GUIFrames.PageTypes.LOGIN] = GUIFrames.LoginPage(root=self, master=self)
        self.pageDict[GUIFrames.PageTypes.USER_MANAGEMENT] = GUIFrames.UserManagementPage(root=self, master=self)
        self.pageDict[GUIFrames.PageTypes.REQUEST_MANAGEMENT] = GUIFrames.RequestManagementPage(root=self, master=self)
        self.pageDict[GUIFrames.PageTypes.REQUEST_REVIEW] = GUIFrames.RequestReviewPage(root=self, master=self)
        self.pageDict[GUIFrames.PageTypes.QUOTE_MANAGEMENT] = GUIFrames.QuoteManagementPage(root=self, master=self)
        self.pageDict[GUIFrames.PageTypes.SUPPLIER_MANAGEMENT] = GUIFrames.SupplierManagementPage(root=self, master=self)
        self.pageDict[GUIFrames.PageTypes.USER_CREATION] = GUIFrames.UserCreationPage(root=self, master=self)
        self.pageDict[GUIFrames.PageTypes.PASSWORD_RESET] = GUIFrames.PasswordResetPage(root=self, master=self)
        self.pageDict[GUIFrames.PageTypes.REQUEST_CREATION] = GUIFrames.RequestCreationPage(root=self, master=self)
        self.pageDict[GUIFrames.PageTypes.ASSIGN_MANAGER] = GUIFrames.AssignClientToManagerPage(root=self, master=self)
        self.pageDict[GUIFrames.PageTypes.CREATE_SUPPLIER_COMPANY] = GUIFrames.AddSupplierPage(root = self, master = self)
        self.pageDict[GUIFrames.PageTypes.ADD_SUPPLIER_ITEMS] = GUIFrames.AddItemPage(root=self, master=self)
        self.pageDict[GUIFrames.PageTypes.MAIN] = GUIFrames.MainPage(root=self, master=self)
        self.active_page = GUIFrames.PageTypes.MAIN #can be changed for debugging
        self.pageDict[self.active_page].grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
    
    def DisplayPage(self, pagetype: GUIFrames.PageTypes) -> None:
        '''Sets the active page based on passed page type'''
        # Error handling and efficiency check
        if pagetype == self.active_page:
            return
        if (pagetype not in self.pageDict):
            print("Requested page type doesnt exist in page dict")
            return
        # Hide all other pages
        for key, page in self.pageDict.items():
            page.grid_forget()
        # Set new page to active
        newpage = self.pageDict[pagetype]
        newpage.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        newpage.LoadPage()
      
        self.active_page = pagetype

    def Login(self, userID: str, password: str) -> None:
        '''Login and handle error popup'''
        try:
            self.sys.SwitchActiveUser(userID, password)
            self.UpdateActiveUser()
            self.DisplayPage(GUIFrames.PageTypes.PLACEHOLDER)
        except Exception as e:
            pu.popupError(e)
    
    def UpdateActiveUser(self) -> None:
        '''Updates gui_data's active user information'''
        # Get active user info from system
        name, userID, pwd, userType = self.sys.GetUserValues(self.sys.active_user)
        # Update gui data
        self.gui_data.active_user_data["name"].set(name.replace("_", " "))
        self.gui_data.active_user_data["id"].set(userID)
        self.gui_data.active_user_data["type"].set(userType)

    def CreateUser(self, userType: Users.UserType, username: str, pwd: str) -> None:
        '''Calls use creation from system and handles error popups'''
        # check if active user has permission
        if(not self.sys.CheckPermissions(perm.MAKE_USER)):
            pu.popupError("Permission Denied!")
            return
        # Data validation
        if (username == ""):
            pu.popupError("Username required")
            return
        if (pwd == ""):
            pu.popupError("Password required")
            return
        # Call user creation from system
        self.sys.CreateNewUser(userType, username.replace(" ", "_"), pwd)
        # Update user data and restore user management page
        self.gui_data.UpdateUserData(self.sys)
        self.DisplayPage(GUIFrames.PageTypes.USER_MANAGEMENT)

    def ResetUserPassword(self, user_ID: str, newpwd: str) -> None:
        '''Calls reset password from system and handles error popups'''
        # check if active user has permission
        if(not self.sys.CheckPermissions(perm.RESET_PASSWORD)):
            pu.popupError("Permission Denied!")
            return
        # Data validation
        if (user_ID == ""):
            pu.popupError("User ID required")
            return
        if (newpwd == ""):
            pu.popupError("Password required")
            return
        # Call Password Reset from system
        try:
            self.sys.ResetPassword(user_ID,newpwd)
            # Update user data and restore user management page
            self.gui_data.UpdateUserData(self.sys)
            self.DisplayPage(GUIFrames.PageTypes.USER_MANAGEMENT)
            pu.popupMessage("Success!")
        except Exception as e:
            pu.popupError(e)
        

    def AssignCliToMana(self, client_ID: str, manager_ID: str) -> None:
        '''Assigns client to manager and handles error popups'''
        # check if active user has permission
        if(not self.sys.CheckPermissions(perm.ASSIGN_CLI_TO_MANA)):
            pu.popupError("Permission Denied!")
            return
        # Data validation
        if (client_ID == ""):
            pu.popupError("Client ID required")
            return
        if (manager_ID == ""):
            pu.popupError("Manager ID required")
            return
        try:
            self.sys.AssignManager(client_ID,manager_ID)
        except Exception as e:
            pu.popupError(e)
       
    def CreateNewSupplier(self,companyName,companyItems):
        '''Create a new Supplier Company'''
        # check if active user has permission
        if(not self.sys.CheckPermissions(perm.ADD_SUPPLIER_ITEM)):
            pu.popupError("Permission Denied!")
            return
        # Data validation
        if (companyName == ""):
            pu.popupError("Company name required")
            return
        if (companyItems == ""):
            pu.popupError("Items required")
            return
        # Call createNewSupplier from system
        try:
            self.sys.createNewSupplier(companyName,companyItems)
            self.gui_data.UpdateSupplierCompanyData(self.sys)
            self.DisplayPage(GUIFrames.PageTypes.SUPPLIER_MANAGEMENT)
            pu.popupMessage("Success!")
        except Exception as e:
            pu.popupError(e)

    def AddSupplierItem(self,companyName,companyItems):
        '''Adds an item(s) to an existing Supplier Company'''
        # check if active user has permission
        if(not self.sys.CheckPermissions(perm.ADD_SUPPLIER_ITEM)):
            pu.popupError("Permission Denied!")
            return
        # Data validation
        if (companyName == ""):
            pu.popupError("Company name required")
            return
        if (companyItems == ""):
            pu.popupError("Items required")
            return
        # Call createNewSupplier from system
        try:
            self.sys.addItemsToCompany(companyName,companyItems)
            self.gui_data.UpdateSupplierCompanyData(self.sys)
            self.DisplayPage(GUIFrames.PageTypes.SUPPLIER_MANAGEMENT)
            pu.popupMessage("Success!")
        except Exception as e:
            pu.popupError(e)


    def CreateProcRequest(self, item: str, qty: str):
        '''Creates a Procurement Request'''
        # check if active user has permission
        if(not self.sys.CheckPermissions(perm.CREATE_REQUEST)):
            pu.popupError("Permission Denied!")
            return
        # Data validation
        if (item == ""):
            pu.popupError("Item required")
            return
        if (qty == ""):
            pu.popupError("Quantity required")
            return
        # call Create Request
        name, userID, pwd, userType = self.sys.GetUserValues(self.sys.active_user)
        try:
            req_no = self.sys.CreateRequest(userID,item,qty)
            self.gui_data.UpdateRequestData(self.sys)
            pu.popupMessage(f"Success! Request {req_no} has been generated")
        except Exception as e:
            pu.popupError(e)
    
    def CreateQuote(self, reqID: str, price: str):
        '''Create quote'''
        if (not self.sys.CheckPermissions(perm.CREATE_QUOTE)):
            pu.popupError("Permission Denied!")
            return
        # Data validation
        if (reqID == ""):
            pu.popupError("Request ID required")
            return
        if (price == ""):
            pu.popupError("Price required")
            return
        price = float(price)
        price = round(price, 2)
        
        if (price <= 0) or (price > 9999999):
            pu.popupError("Invalid price")
            return

        #reqID, itemName, quantity, generatedByID, assignedManagerID, status, acceptedQuoteID
        try:
            # reqID_temp, itemName, quantity, generatedByID, assignedManagerID, status, acceptedQuoteID = self.sys.database.get_request(f"{reqID}")
            quoteID = self.sys.CreateQuote(price, reqID)
            self.gui_data.UpdateQuotesManagerData(self.sys)
            pu.popupMessage(f"Success! Quote {quoteID} has been generated")
        except Exception as e:
            pu.popupError(e)
    
    def AcceptQuote(self, quoteID: str) -> None:
        if(not self.sys.CheckPermissions(perm.ACCEPT_REJECT)):
            pu.popupError("Permission Denied!")
            return
        if (quoteID == ""):
            pu.popupError("Quote ID required")
            return
        try:
            activeUserID = self.sys.active_user
            reqID = self.sys.database.get_request_id_from_quote(quoteID)
            reqID_temp, itemName, quantity, generatedByID, assignedManagerID, status, acceptedQuoteID = self.sys.database.get_request(reqID)
            if (activeUserID != assignedManagerID):
                raise Exception(f"Active user is not assigned to request {reqID}")
            self.sys.ManagerAcceptQuote(quoteID)
            self.pageDict[self.active_page].LoadPage()
        except Exception as e:
            pu.popupError(e)

    def RejectRequest(self, reqID: str) -> None:
        if(not self.sys.CheckPermissions(perm.ACCEPT_REJECT)):
            pu.popupError("Permission Denied!")
            return
        if (reqID == ""):
            pu.popupError("Request ID required")
            return
        try:
            activeUserID = self.sys.active_user
            reqID_temp, itemName, quantity, generatedByID, assignedManagerID, status, acceptedQuoteID = self.sys.database.get_request(reqID)
            if (activeUserID != assignedManagerID):
                raise Exception(f"Active user is not assigned to request {reqID}")
            self.sys.ManagerDenyRequest(reqID)
            self.pageDict[self.active_page].LoadPage()
        except Exception as e:
            pu.popupError(e)

if __name__ == "__main__": 
    app = ProcSysGUI()
    app.mainloop()
