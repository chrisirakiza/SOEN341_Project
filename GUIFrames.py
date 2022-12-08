import customtkinter as ctk
from enum import Enum
from PIL import Image, ImageTk
import os
import Users
import PopUp as pu
from Permissions import FunctionTypes as perm

PATH = os.path.dirname(os.path.realpath(__file__))

class PageTypes(Enum):
    PLACEHOLDER = 0
    LOGIN = 1
    USER_MANAGEMENT = 2
    REQUEST_MANAGEMENT = 3
    REQUEST_REVIEW = 4
    QUOTE_MANAGEMENT = 5
    SUPPLIER_MANAGEMENT = 6
    USER_CREATION = 7
    MAIN = 8
    PASSWORD_RESET = 9
    REQUEST_CREATION = 10
    ASSIGN_MANAGER = 11
    CREATE_SUPPLIER_COMPANY = 12
    ADD_SUPPLIER_ITEMS = 13

class Page(ctk.CTkFrame):
    def __init__(self, root, *args, **kwargs):
        ctk.CTkFrame.__init__(self, *args, **kwargs)
        self.root = root
    def show(self):
        self.lift()
    def LoadPage(self):
        pass

class MainPage(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        logo_icon = load_image("/GUI_images/logo.png", 300)
        lbl_logo = ctk.CTkButton(master=self, image=logo_icon, text="", width=310, height=310)
        lbl_logo.pack(pady=(100, 0))
        lbl_title = ctk.CTkLabel(master=self, text="Amogus Inc.")
        lbl_title.configure(font=("Arial", 33))
        lbl_title.pack(pady=10)


class NavBar(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)  
        self.grid_rowconfigure(1, weight=1)

        # Populated with user box and navigation selector
        NavBar_UserBox(root=self.root, master=self, height=100).grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
        NavBar_Selector(root=self.root, master=self).grid(row=1, column=0, sticky="nswe", padx=10, pady=10)

class NavBar_UserBox(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        # Configure grid
        self.grid_columnconfigure(1, weight=1)  
        self.grid_rowconfigure(0, weight=1)

        # Login button
        user_icon = load_image("/GUI_images/user-icon.png", 30)
        btn_user = ctk.CTkButton(master=self, image=user_icon, text="", command=lambda: self.root.DisplayPage(PageTypes.LOGIN), width=40, height=40)
        btn_user.grid(row=0, column=0)
        
        lbl_username = ctk.CTkLabel(self, textvariable=self.root.gui_data.active_user_data["name"])
        lbl_username.grid(row=0, column=1)
            

class NavBar_Selector(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        # User Management Button
        btn_user_mana = ctk.CTkButton(master=self, text = "User Management", command=lambda: user_mana_btn_controller(self)) 
        btn_user_mana.pack(pady = 15, fill = "both", side="top")

        # Request Management Button
        btn_req_mana = ctk.CTkButton(master=self, text = "Request Management", command=lambda: req_mana_btn_controller(self))
        btn_req_mana.pack(pady = 15, fill = "both", side="top")

        # Request Review Button
        btn_req_rev = ctk.CTkButton(master=self, text = "Request Review", command=lambda: req_rev_btn_controller(self))
        btn_req_rev.pack(pady = 15, fill = "both", side="top")

        # Quote Management Button
        btn_quo_mana = ctk.CTkButton(master=self, text = "Quote Management",command=lambda: quo_mana_btn_controller(self))
        btn_quo_mana.pack(pady = 15, fill = "both", side="top")    

        # Supplier Management Button
        btn_sup_mana = ctk.CTkButton(master=self, text = "Supplier Management",command=lambda: sup_mana_btn_controller(self))
        btn_sup_mana.pack(pady = 15, fill = "both", side="top")  

        def user_mana_btn_controller(self):
            if(not self.root.sys.CheckPermissions(perm.ACCESS_USER_MANAGEMENT)):
                pu.popupError("Permission Denied")
            else:
                self.root.DisplayPage(PageTypes.USER_MANAGEMENT)
        def req_mana_btn_controller(self):
            if(not self.root.sys.CheckPermissions(perm.ACCESS_REQUEST_MANAGEMENT)):
                pu.popupError("Permission Denied")
            else:
                self.root.DisplayPage(PageTypes.REQUEST_MANAGEMENT)
       
        def req_rev_btn_controller(self):
            if(not self.root.sys.CheckPermissions(perm.ACCESS_REQUEST_REVIEW)):
                pu.popupError("Permission Denied")
            else:
                self.root.DisplayPage(PageTypes.REQUEST_REVIEW)
        
        def quo_mana_btn_controller(self):
            if(not self.root.sys.CheckPermissions(perm.ACCESS_QUOTE_MANAGEMENT)):
                pu.popupError("Permission Denied")
            else:
                self.root.DisplayPage(PageTypes.QUOTE_MANAGEMENT)
        def sup_mana_btn_controller(self):
            if(not self.root.sys.CheckPermissions(perm.ACCESS_SUPPLIER_MANAGEMENT)):
                pu.popupError("Permission Denied")
            else:
                self.root.DisplayPage(PageTypes.SUPPLIER_MANAGEMENT)
     

class LoginPage(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        # Exit button
        exit_icon = load_image("/GUI_images/exit.png", 30)
        btn_exit = ctk.CTkButton(master=self, image=exit_icon, text="", command=lambda: self.root.DisplayPage(PageTypes.MAIN), width=38)
        btn_exit.pack(side=ctk.TOP, anchor=ctk.NW, pady=10, padx=10)

        lbl_placeholder = ctk.CTkLabel(self, text="User Login")
        lbl_placeholder.pack(pady=(50,0))
        ent_userID = ctk.CTkEntry(master=self, width=300, placeholder_text="User ID")
        ent_userID.pack(pady=10)  
        ent_password = ctk.CTkEntry(master=self, width=300, placeholder_text="Password", show="*")
        ent_password.pack(pady=10)
        btn_login = ctk.CTkButton(master=self, text="Login", command=lambda: [self.root.Login(ent_userID.get(), ent_password.get()),
                                                                             ent_userID.delete(0,"end"),
                                                                             ent_password.delete(0,"end")])
        btn_login.pack(pady=10)   

class PlaceHolderPage(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        lbl_placeholder = ctk.CTkLabel(self, text="Placeholder")
        lbl_placeholder.pack()

class UserManagementPage(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        self.table_rows = 11
        self.table_cols = 5
        self.access = perm.ACCESS_USER_MANAGEMENT

        # Configure grid
        self.grid_columnconfigure(0, weight=1, uniform="column")
        self.grid_rowconfigure(2, weight=1)
        # Add page label
        lbl_usermanagment = ctk.CTkLabel(self, text="User Management")
        lbl_usermanagment.grid(row=0, column=0, pady=(10,0))
        # Create table frame
        self.frame_table = ctk.CTkFrame(master=self) #frame for listing tables
        self.frame_table.grid(row=1, column=0, sticky="nswe", padx=10, pady=10)
        self.frame_table.columnconfigure(self.table_cols-1, weight=1)
        self.frame_table.rowconfigure(self.table_rows-1, weight=1)
        # Create button frame
        self.frame_button = ctk.CTkFrame(master=self, height=10, corner_radius=0) #frame hosting buttons
        self.frame_button.grid(row=2, column=0, sticky="nswe", pady=10)
        self.frame_button.columnconfigure(1, weight=1)
        self.frame_button.rowconfigure(1, weight=1)
        
        # Populate button frame
        add_user_icon = load_image("/GUI_images/add-user.png", 30)
        btn_add_user = ctk.CTkButton(master=self.frame_button, image=add_user_icon, text="Add User", command=lambda: self.root.DisplayPage(PageTypes.USER_CREATION))
        btn_add_user.grid(row=0, column=0, sticky="w", padx=(100, 10),pady = 10)
        btn_assign_mana = ctk.CTkButton(master=self.frame_button, text="Assign Client To Manager",command=lambda: self.root.DisplayPage(PageTypes.ASSIGN_MANAGER))
        btn_assign_mana.grid(row=1, column=0, sticky="w", padx=(100, 10))
        reset_password_icon = load_image("/GUI_images/loop-circular.png", 30)
        btn_reset_password = ctk.CTkButton(master=self.frame_button, image=reset_password_icon , text="Reset User Password", command=lambda: self.root.DisplayPage(PageTypes.PASSWORD_RESET))
        btn_reset_password.grid(row=0, column=1, sticky="e", padx=(10, 100),pady = 10)

        # Set up table
        lbl_id = ctk.CTkLabel(master=self.frame_table, text="ID")
        lbl_id.grid(row=0, column=0, sticky='EW')
        lbl_name = ctk.CTkLabel(master=self.frame_table, text="Name")
        lbl_name.grid(row=0, column=1, sticky='EW')
        lbl_type = ctk.CTkLabel(master=self.frame_table, text="Type")
        lbl_type.grid(row=0, column=2, sticky='EW')
        lbl_manager = ctk.CTkLabel(master=self.frame_table, text="Managed By")
        lbl_manager.grid(row=0, column=3, sticky='EW')
        lbl_manager = ctk.CTkLabel(master=self.frame_table, text="Company")
        lbl_manager.grid(row=0, column=4, sticky='EW')
        self.PopulateTable()

    def LoadPage(self):
        super().LoadPage()
        self.root.gui_data.UpdateUserData(self.root.sys)
        self.PopulateTable()

    def PopulateTable(self):
        '''Populates the table using GUI data from the root'''
        users_in_database = len(self.root.gui_data.users_data)
        for i in range(1, self.table_rows):
            if (i > users_in_database):
                for j in range (0, self.table_cols):
                    lblTemp = ctk.CTkLabel(master=self.frame_table, text="")
                    lblTemp.grid(row=i, column=j, sticky='EW')
            else:
                for j in range (0, self.table_cols):
                    lblTemp = ctk.CTkLabel(master=self.frame_table, textvariable=self.root.gui_data.users_data[i-1][j])
                    lblTemp.grid(row=i, column=j, sticky='EW')

class UserCreationPage(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        # Exit button
        exit_icon = load_image("/GUI_images/exit.png", 30)
        btn_exit = ctk.CTkButton(master=self, image=exit_icon, text="", command=lambda: self.root.DisplayPage(PageTypes.USER_MANAGEMENT), width=38)
        btn_exit.pack(side=ctk.TOP, anchor=ctk.NW, pady=10, padx=10)
        # Page label
        lbl_placeholder = ctk.CTkLabel(self, text="User Create")
        lbl_placeholder.pack(pady=(50,0))
        # Username and password entry
        ent_username = ctk.CTkEntry(master=self, width=300, placeholder_text="Username")
        ent_username.pack(pady=10)  
        ent_password = ctk.CTkEntry(master=self, width=300, placeholder_text="Password", show="*")
        ent_password.pack(pady=10)
        # Type selector
        userTypes = ["Client", "Manager", "Supplier", "Admin"]
        cbo_type = ctk.CTkComboBox(master=self, values=userTypes)
        cbo_type.pack(pady=10)
        # Create user button
        btn_create = ctk.CTkButton(master=self, text="Create", command=lambda: [self.root.CreateUser(Users.UserType.ParseUserType(cbo_type.get()), ent_username.get(), ent_password.get()),
                                                                                ent_username.delete(0,"end"),
                                                                                ent_password.delete(0,"end")])
        btn_create.pack(pady=10)

class AssignClientToManagerPage(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        # Exit button
        exit_icon = load_image("/GUI_images/exit.png", 30)
        btn_exit = ctk.CTkButton(master=self, image=exit_icon, text="", command=lambda: self.root.DisplayPage(PageTypes.USER_MANAGEMENT), width=38)
        btn_exit.pack(side=ctk.TOP, anchor=ctk.NW, pady=10, padx=10)
        # Page label
        lbl_placeholder = ctk.CTkLabel(self, text="Assign Client to Manager")
        lbl_placeholder.pack(pady=(50,0))
        # Username and password entry
        ent_clientID = ctk.CTkEntry(master=self, width=300, placeholder_text="Client ID")
        ent_clientID.pack(pady=10)  
        ent_manaID = ctk.CTkEntry(master=self, width=300, placeholder_text="Manager ID")
        ent_manaID.pack(pady=10)
        # Confirm Button
        btn_confirm = ctk.CTkButton(master=self, text="Confirm", command = lambda: [self.root.AssignCliToMana(ent_clientID.get(),ent_manaID.get()),
                                                                                    ent_clientID.delete(0,"end"),
                                                                                    ent_manaID.delete(0,"end")])
        btn_confirm.pack(pady=10)

class PasswordResetPage(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        # Exit button
        exit_icon = load_image("/GUI_images/exit.png", 30)
        btn_exit = ctk.CTkButton(master=self, image=exit_icon, text="", command=lambda: self.root.DisplayPage(PageTypes.USER_MANAGEMENT), width=38)
        btn_exit.pack(side=ctk.TOP, anchor=ctk.NW, pady=10, padx=10)
        # Page label
        lbl_placeholder = ctk.CTkLabel(self, text="Password Reset")
        lbl_placeholder.pack(pady=(50,0))
        # Username and password entry
        ent_userID = ctk.CTkEntry(master=self, width=300, placeholder_text="User ID")
        ent_userID.pack(pady=10)  
        ent_newPassword = ctk.CTkEntry(master=self, width=300, placeholder_text="New Password", show="*")
        ent_newPassword.pack(pady=10)
        # Confirm Button
        btn_confirm = ctk.CTkButton(master=self, text="Confirm",command = lambda: [self.root.ResetUserPassword(ent_userID.get(),ent_newPassword.get()),
                                                                                    ent_userID.delete(0,"end"),
                                                                                    ent_newPassword.delete(0,"end")])
        btn_confirm.pack(pady=10)

class RequestManagementPage(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)
        
        self.grid_columnconfigure(0,weight = 1)
        self.grid_rowconfigure(2,weight = 1)
        self.table_rows = 11
        self.table_cols = 7
        self.access = perm.ACCESS_REQUEST_MANAGEMENT
        
        lbl_reqmanagement = ctk.CTkLabel(self, text="Request Management")
        lbl_reqmanagement.grid(row = 0, column = 0)

        #set Parent grid
        self.frame_button = ctk.CTkFrame(master = self, height=100,width=750) #frame hosting buttons
        self.frame_button.grid(row = 2, column = 0, sticky = "nswe", padx=10, pady=10)
        self.frame_button.columnconfigure(1,weight = 1)
        self.frame_button.rowconfigure(0,weight = 1)
        self.frame_table = ctk.CTkFrame(master = self) #frame for listing tables
        self.frame_table.grid(row = 1, column = 0, sticky = "nswe", padx=10, pady=10)
        self.frame_table.columnconfigure(self.table_cols-1,weight = 1)
        self.frame_table.rowconfigure(self.table_rows-1,weight = 1)

       
        btn_new_req = ctk.CTkButton(master=self.frame_button, text = "Create New Request", command=lambda: self.root.DisplayPage(PageTypes.REQUEST_CREATION))
        btn_new_req.grid(row = 1, column = 0)
        
         #define filter button to view user-generated requests
        chkbx_show_created = ctk.CTkCheckBox(master=self.frame_button, text = "Show My Requests")
        chkbx_show_created.grid(row=0,column = 0,sticky = "nw")
       
        #initialize table header
        lbl_id = ctk.CTkLabel(master = self.frame_table, text = "Request ID")
        lbl_id.grid(row = 0, column = 0)
        lbl_item = ctk.CTkLabel(master = self.frame_table, text = "Item")
        lbl_item.grid(row = 0, column = 1)
        lbl_qty = ctk.CTkLabel(master = self.frame_table, text = "Qty")
        lbl_qty.grid(row = 0, column = 2)
        lbl_client = ctk.CTkLabel(master = self.frame_table, text = "Generated By")
        lbl_client.grid(row = 0, column = 3)
        lbl_manager = ctk.CTkLabel(master = self.frame_table, text = "Assigned Manager")
        lbl_manager.grid(row = 0, column = 4)
        lbl_status = ctk.CTkLabel(master = self.frame_table, text = "Request Status")
        lbl_status.grid(row = 0, column = 5)
        lbl_acccepted_quote = ctk.CTkLabel(master = self.frame_table, text = "Accepted Quote #")
        lbl_acccepted_quote.grid(row = 0, column = 6)
        self.PopulateTable()
        
    def LoadPage(self):
        super().LoadPage()
        self.root.gui_data.UpdateRequestData(self.root.sys)
        self.PopulateTable()
        
    def PopulateTable(self):
        '''Populates the table using GUI data from the root'''
        requests_in_database = len(self.root.gui_data.requests_data)
        print(f"Lenght: {requests_in_database}")
        for i in range(1, self.table_rows):
            if (i > requests_in_database):
                for j in range (0, self.table_cols):
                    lblTemp = ctk.CTkLabel(master=self.frame_table, text="")
                    lblTemp.grid(row=i, column=j, sticky='EW')
            else:
                for j in range (0, self.table_cols):
                    lblTemp = ctk.CTkLabel(master=self.frame_table, textvariable=self.root.gui_data.requests_data[i-1][j])
                    lblTemp.grid(row=i, column=j, sticky='EW')
        

class RequestCreationPage(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        # Exit button
        exit_icon = load_image("/GUI_images/exit.png", 30)
        btn_exit = ctk.CTkButton(master=self, image=exit_icon, text="", command=lambda: self.root.DisplayPage(PageTypes.REQUEST_MANAGEMENT), width=38)
        btn_exit.pack(side=ctk.TOP, anchor=ctk.NW, pady=10, padx=10)
        # Page label
        lbl_placeholder = ctk.CTkLabel(self, text="Create a Procurement Request")
        lbl_placeholder.pack(pady=(50,0))
        # Item Type and Quantity
        ent_Item = ctk.CTkEntry(master=self, width=300, placeholder_text="Item Name")
        ent_Item.pack(pady=10)  
        ent_Quantity = ctk.CTkEntry(master=self, width=90, placeholder_text="Quantity")
        ent_Quantity.pack(pady=10)
        # Confirm Button
        btn_create = ctk.CTkButton(master=self, text="Confirm",command=lambda:[self.root.CreateProcRequest(ent_Item.get(),ent_Quantity.get()),
                                                                                    ent_Item.delete(0,"end"),
                                                                                    ent_Quantity.delete(0, "end")])
        btn_create.pack(pady=10)

class RequestReviewPage(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)
        self.grid_columnconfigure(0,weight = 1)
        self.grid_rowconfigure(2,weight = 1)
        self.access = perm.ACCESS_REQUEST_REVIEW
        # Table geom
        self.tableRows = 11
        self.tableCols = 8

        lbl_reqmanagement = ctk.CTkLabel(self, text="Request Review")
        lbl_reqmanagement.grid(row = 0, column = 0)

        #set Parent grid
        frame_bottom = ctk.CTkFrame(master = self, height=100,width=750) 
        frame_bottom.grid(row = 2, column = 0, sticky = "nswe", padx=10, pady=10)
        frame_bottom.columnconfigure(2,weight = 1)
        frame_bottom.rowconfigure(1,weight = 1)
        self.frame_table = ctk.CTkFrame(master = self) #frame for listing tables
        self.frame_table.grid(row = 1, column = 0, sticky = "nswe", padx=10, pady=10)
        self.frame_table.columnconfigure(self.tableCols - 1, weight = 1)
        self.frame_table.rowconfigure(self.tableRows - 1, weight = 1)
        
        #define filter to show assigned requests
        chkbx_show_assigned = ctk.CTkCheckBox(master = frame_bottom, text = "Show Assigned")
        chkbx_show_assigned.grid(row = 0, column = 0, sticky = "nw")

        quoteIDField = ctk.CTkEntry(master = frame_bottom, width=150, placeholder_text="Quote/Request ID")
        quoteIDField.grid(row = 1, column = 0)

        #define buttons for acepting/rejecting requests
        accept_btn = ctk.CTkButton(master = frame_bottom, text = "Accept Quote",text_color= "green", command=lambda:[self.root.AcceptQuote(quoteIDField.get()),
                                                                                    quoteIDField.delete(0,"end"),self.LoadPage()])
        accept_btn.grid(row = 1, column = 1, padx = 15)
        reject_btn = ctk.CTkButton(master = frame_bottom, text = "Reject Request",text_color= "red", command=lambda:[self.root.RejectRequest(quoteIDField.get()),
                                                                                    quoteIDField.delete(0,"end"),self.LoadPage()])
        reject_btn.grid(row = 1, column = 2, padx = 15)

       #initialize table header
       # [quoteID, reqID, itemName, itemQuantity, price, generatedBy, managerID, supplierID]
        lbl_id = ctk.CTkLabel(master = self.frame_table, text = "Quote ID")
        lbl_id.grid(row = 0, column = 0)
        lbl_item = ctk.CTkLabel(master = self.frame_table, text = "Request ID")
        lbl_item.grid(row = 0, column = 1)
        lbl_qty = ctk.CTkLabel(master = self.frame_table, text = "Item")
        lbl_qty.grid(row = 0, column = 2)
        lbl_client = ctk.CTkLabel(master = self.frame_table, text = "Qty")
        lbl_client.grid(row = 0, column = 3)
        lbl_manager = ctk.CTkLabel(master = self.frame_table, text = "Price")
        lbl_manager.grid(row = 0, column = 4)
        lbl_status = ctk.CTkLabel(master = self.frame_table, text = "Req Generated By")
        lbl_status.grid(row = 0, column = 5)
        lbl_acccepted_quote = ctk.CTkLabel(master = self.frame_table, text = "Assigned Manager")
        lbl_acccepted_quote.grid(row = 0, column = 6)
        lbl_acccepted_quote = ctk.CTkLabel(master = self.frame_table, text = "Quote Generated By")
        lbl_acccepted_quote.grid(row = 0, column = 7)
        self.PopulateTable()
        
    def LoadPage(self):
        super().LoadPage()
        self.root.gui_data.UpdateQuotesManagerData(self.root.sys)
        self.PopulateTable()
    
    def PopulateTable(self):
        '''Populates the table using GUI data from the root'''
        quotes_in_database = len(self.root.gui_data.quotes_data)
        for i in range(1, self.tableRows):
            if (i > quotes_in_database):
                for j in range (0, self.tableCols):
                    lblTemp = ctk.CTkLabel(master=self.frame_table, text="")
                    lblTemp.grid(row=i, column=j, sticky='EW')
            else:
                for j in range (0, self.tableCols):
                    lblTemp = ctk.CTkLabel(master=self.frame_table, textvariable=self.root.gui_data.quotes_data[i-1][j])
                    lblTemp.grid(row=i, column=j, sticky='EW')

class QuoteManagementPage(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)
        
        self.grid_columnconfigure(0,weight = 1)
        self.grid_rowconfigure(2,weight = 1)
        self.access = perm.ACCESS_QUOTE_MANAGEMENT

        # Table geom
        self.tableRows = 11
        self.tableCols = 3

        lbl_reqmanagement = ctk.CTkLabel(self, text="Quote Management")
        lbl_reqmanagement.grid(row = 0, column = 0)

        #set Parent grid
        frame_bottom = ctk.CTkFrame(master = self, height=100,width=750) #frame hosting buttons
        frame_bottom.grid(row = 2, column = 0, sticky = "nswe", padx=10, pady=10)
        frame_bottom.columnconfigure(1,weight = 1)
        frame_bottom.rowconfigure(1,weight = 1)
        self.frame_table = ctk.CTkFrame(master = self) #frame for listing tables
        self.frame_table.grid(row = 1, column = 0, sticky = "nswe", padx=10, pady=10)
        self.frame_table.columnconfigure(self.tableCols - 1, weight = 1)
        self.frame_table.rowconfigure(self.tableRows, weight = 1)

        #configure list for drop down list
        requestIDField = ctk.CTkEntry(master = frame_bottom, width=100, placeholder_text="Request ID")
        requestIDField.grid(row = 0,column = 0, sticky = "w", pady = 15, padx=15)

        priceTextField = ctk.CTkEntry(master = frame_bottom, width=100, placeholder_text="Quote Price")
        priceTextField.grid(row = 1, column = 1, sticky = "n", pady = 15, padx=15)

        sendButton = ctk.CTkButton(master = frame_bottom,text = "Send Quote", command=lambda:[self.root.CreateQuote(requestIDField.get(),priceTextField.get()),
                                                                                    requestIDField.delete(0,"end"),
                                                                                    priceTextField.delete(0, "end"),self.LoadPage()])
        sendButton.grid(row = 2, column = 2, sticky = "n", pady = 15, padx=15)
       
        lbl_id = ctk.CTkLabel(master = self.frame_table, text = "Request ID")
        lbl_id.grid(row = 0, column = 0)
        lbl_item = ctk.CTkLabel(master = self.frame_table, text = "Item")
        lbl_item.grid(row = 0, column = 1)
        lbl_qty = ctk.CTkLabel(master = self.frame_table, text = "Qty")
        lbl_qty.grid(row = 0, column = 2)
        self.PopulateTable()
        
    def LoadPage(self):
        super().LoadPage()
        self.root.gui_data.UpdateRequestDataSuppliers(self.root.sys)
        print(self.root.gui_data.requests_data_suppliers)
        self.PopulateTable()
        
    def PopulateTable(self):
        '''Populates the table using GUI data from the root'''
        requests_in_database = len(self.root.gui_data.requests_data_suppliers)
        for i in range(1, self.tableRows):
            if (i > requests_in_database):
                for j in range (0, self.tableCols):
                    lblTemp = ctk.CTkLabel(master=self.frame_table, text="")
                    lblTemp.grid(row=i, column=j, sticky='EW')
            else:
                for j in range (0, self.tableCols):
                    lblTemp = ctk.CTkLabel(master=self.frame_table, textvariable=self.root.gui_data.requests_data_suppliers[i-1][j])
                    lblTemp.grid(row=i, column=j, sticky='EW')

class SupplierManagementPage(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)
        self.grid_columnconfigure(0,weight = 1)
        self.grid_rowconfigure(2,weight = 1)
        self.tableRows = 11
        self.tableCols = 2
        self.access = perm.ACCESS_SUPPLIER_MANAGEMENT

        lbl_reqmanagement = ctk.CTkLabel(self, text="Supplier Management")
        lbl_reqmanagement.grid(row = 0, column = 0)

        # #set Parent grid
        frame_button = ctk.CTkFrame(master = self, height=100,width=750) #frame hosting buttons
        frame_button.grid(row = 2, column = 0, sticky = "nswe", padx=10, pady=10)
        frame_button.columnconfigure(2,weight = 1)
        frame_button.rowconfigure(0,weight = 1)
        self.frame_table = ctk.CTkFrame(master = self) #frame for listing tables
        self.frame_table.grid(row = 1, column = 0, sticky = "nswe", padx=10, pady=10)
        self.frame_table.columnconfigure(1,weight = 1)
        self.frame_table.rowconfigure(10,weight = 1)

        btn_new_supplier = ctk.CTkButton(master=frame_button, text = "Add New Supplier",command=lambda:self.root.DisplayPage(PageTypes.CREATE_SUPPLIER_COMPANY))
        btn_new_supplier.grid(row = 0, column = 0)
        btn_add_item = ctk.CTkButton(master = frame_button, text = "Add New Item",command=lambda:self.root.DisplayPage(PageTypes.ADD_SUPPLIER_ITEMS))
        btn_add_item. grid(row = 0, column = 1,sticky = "e")
       
        lbl_id = ctk.CTkLabel(master = self.frame_table, text = "Supplier")
        lbl_id.grid(row = 0, column = 0)
        lbl_item = ctk.CTkLabel(master = self.frame_table, text = "Items")
        lbl_item.grid(row = 0, column = 1)
        self.PopulateTable()
        
    def LoadPage(self):
        super().LoadPage()
        self.root.gui_data.UpdateSupplierCompanyData(self.root.sys)
        self.PopulateTable()
        
    def PopulateTable(self):
        '''Populates the table using GUI data from the root'''
        companies_in_database = len(self.root.gui_data.supplier_company_data)
        for i in range(1, self.tableRows):
            if (i > companies_in_database):
                for j in range (0, self.tableCols):
                    lblTemp = ctk.CTkLabel(master=self.frame_table, text="")
                    lblTemp.grid(row=i, column=j, sticky='EW')
            else:
                for j in range (0, self.tableCols):
                    lblTemp = ctk.CTkLabel(master=self.frame_table, textvariable=self.root.gui_data.supplier_company_data[i-1][j])
                    lblTemp.grid(row=i, column=j, sticky='EW')

#Add a supplier company to the database
class AddSupplierPage(Page):
    def __init__(self, root, *args, **kwargs):
       Page.__init__(self, root, *args, **kwargs)
       # Exit button
       exit_icon = load_image("/GUI_images/exit.png", 30)
       btn_exit = ctk.CTkButton(master=self, image=exit_icon, text="", command=lambda: self.root.DisplayPage(PageTypes.SUPPLIER_MANAGEMENT), width=38)
       btn_exit.pack(side=ctk.TOP, anchor=ctk.NW, pady=10, padx=10)

       lbl_placeholder = ctk.CTkLabel(self, text="Add Supplier")
       lbl_placeholder.pack(pady=(50,0))
       ent_companyName = ctk.CTkEntry(master=self, width=300, placeholder_text="Company Name")
       ent_companyName.pack(pady=10)  
       ent_companyItems = ctk.CTkEntry(master=self, width=900,placeholder_text="Item(s)")
       ent_companyItems.pack(pady=10)
       btn_confirm = ctk.CTkButton(master=self, text="Confirm", command=lambda: ([self.root.CreateNewSupplier(ent_companyName.get(),ent_companyItems.get()),
                                                                             ent_companyName.delete(0,"end"),
                                                                             ent_companyItems.delete(0,"end")]))

       btn_confirm.pack(pady=10)  

#Add an item to supplier company in the database
class AddItemPage(Page):
    def __init__(self, root, *args, **kwargs):
       Page.__init__(self, root, *args, **kwargs)
       # Exit button
       exit_icon = load_image("/GUI_images/exit.png", 30)
       btn_exit = ctk.CTkButton(master=self, image=exit_icon, text="", command=lambda: self.root.DisplayPage(PageTypes.SUPPLIER_MANAGEMENT), width=38)
                                                                                    
       btn_exit.pack(side=ctk.TOP, anchor=ctk.NW, pady=10, padx=10)

       lbl_placeholder = ctk.CTkLabel(self, text="Add Item")
       lbl_placeholder.pack(pady=(50,0))
       ent_companyName = ctk.CTkEntry(master=self, width=300, placeholder_text="Company Name")
       ent_companyName.pack(pady=10)  
       ent_companyItems = ctk.CTkEntry(master=self, width=900,placeholder_text="Item(s) to Add")
       ent_companyItems.pack(pady=10)
       btn_confirm = ctk.CTkButton(master=self, text="Confirm", command=lambda: ([self.root.AddSupplierItem(ent_companyName.get(),ent_companyItems.get()),
                                                                             ent_companyName.delete(0,"end"),
                                                                             ent_companyItems.delete(0,"end")]))

       btn_confirm.pack(pady=10)  

def load_image(path, image_size):
        """ Load image """
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size, image_size)))

