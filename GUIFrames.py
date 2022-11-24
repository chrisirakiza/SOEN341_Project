import customtkinter as ctk
from enum import Enum
from PIL import Image, ImageTk
import os

PATH = os.path.dirname(os.path.realpath(__file__))

class PageTypes(Enum):
    PLACEHOLDER = 0
    LOGIN = 1
    USER_MANAGEMENT = 2
    REQUEST_MANAGEMENT = 3
    REQUEST_REVIEW = 4
    QUOTE_MANAGEMENT = 5
    SUPPLIER_MANAGEMENT =6

class Page(ctk.CTkFrame):
    def __init__(self, root, *args, **kwargs):
        ctk.CTkFrame.__init__(self, *args, **kwargs)
        self.root = root
    def show(self):
        self.lift()

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
        btn_user_mana = ctk.CTkButton(master=self, text = "User Management", command=lambda: self.root.DisplayPage(PageTypes.USER_MANAGEMENT)) #needs to be linked
        btn_user_mana.pack(pady = 15, fill = "both", side="top")

        # Request Management Button
        btn_req_mana = ctk.CTkButton(master=self, text = "Request Management", command=lambda: self.root.DisplayPage(PageTypes.REQUEST_MANAGEMENT)) #needs to be linked
        btn_req_mana.pack(pady = 15, fill = "both", side="top")

        # Request Review Button
        btn_req_rev = ctk.CTkButton(master=self, text = "Request Review", command=lambda: self.root.DisplayPage(PageTypes.REQUEST_REVIEW)) #needs to be linked
        btn_req_rev.pack(pady = 15, fill = "both", side="top")

        # Quote Management Button
        btn_quo_mana = ctk.CTkButton(master=self, text = "Quote Management",command=lambda: self.root.DisplayPage(PageTypes.QUOTE_MANAGEMENT)) #needs to be linked
        btn_quo_mana.pack(pady = 15, fill = "both", side="top")    

        # Supplier Management Button
        btn_sup_mana = ctk.CTkButton(master=self, text = "Supplier Management",command=lambda: self.root.DisplayPage(PageTypes.SUPPLIER_MANAGEMENT)) #needs to be linked
        btn_sup_mana.pack(pady = 15, fill = "both", side="top")    
     

class LoginPage(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        lbl_placeholder = ctk.CTkLabel(self, text="User Login")
        lbl_placeholder.pack(pady=(50,0))
        ent_userID = ctk.CTkEntry(master=self, width=300, placeholder_text="User ID")
        ent_userID.pack(pady=10)  
        ent_password = ctk.CTkEntry(master=self, width=300, placeholder_text="Password", show="*")
        ent_password.pack(pady=10)
        btn_login = ctk.CTkButton(master=self, text="Login", command=lambda: self.root.Login(ent_userID.get(), ent_password.get()))
        btn_login.pack(pady=10)   

class PlaceHolderPage(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        lbl_placeholder = ctk.CTkLabel(self, text="Placeholder")
        lbl_placeholder.pack()

class UserManagementPage(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)
        self.grid_columnconfigure(0,weight = 1)
        self.grid_rowconfigure(2,weight = 1)
       
        lbl_usermanagment = ctk.CTkLabel(self, text="User Management")
        lbl_usermanagment.grid(row = 0, column = 0)

        #set Parent grid
        frame_button = ctk.CTkFrame(master = self, height=100,width=750) #frame hosting buttons
        frame_button.grid(row = 2, column = 0, sticky = "nswe", padx=10, pady=10)
        frame_button.columnconfigure(1,weight = 1)
        frame_button.rowconfigure(0,weight = 1)
        frame_table = ctk.CTkFrame(master = self) #frame for listing tables
        frame_table.grid(row = 1, column = 0, sticky = "nswe", padx=10, pady=10)
        frame_table.columnconfigure(4,weight = 1)
        frame_table.rowconfigure(10,weight = 1)
        
        btn_add_user = ctk.CTkButton(master=frame_button, text = "Add User")
        btn_add_user.grid(row = 0, column = 0,sticky = "w")
        btn_reset_password = ctk.CTkButton(master=frame_button, text = "Reset User Password")
        btn_reset_password.grid(row = 0, column = 1, sticky = "e")

        lbl_id = ctk.CTkLabel(master = frame_table, text = "ID")
        lbl_id.grid(row = 0, column = 0)
        lbl_name = ctk.CTkLabel(master = frame_table, text = "Name")
        lbl_name.grid(row = 0, column = 1)
        lbl_type = ctk.CTkLabel(master = frame_table, text = "Type")
        lbl_type.grid(row = 0, column = 2)
        lbl_manager = ctk.CTkLabel(master = frame_table, text = "Managed By")
        lbl_manager.grid(row = 0, column = 3)
        lbl_manager = ctk.CTkLabel(master = frame_table, text = "Company")
        lbl_manager.grid(row = 0, column = 4)

        for i in range (1, 11):
            for j in range (0,5):
                lblTemp = ctk.CTkLabel(master = frame_table, text = "Jo Mama")
                lblTemp.grid(row = i, column = j)

class RequestManagementPage(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)
        self.grid_columnconfigure(0,weight = 1)
        self.grid_rowconfigure(2,weight = 1)

        lbl_reqmanagement = ctk.CTkLabel(self, text="Request Management")
        lbl_reqmanagement.grid(row = 0, column = 0)

        #set Parent grid
        frame_button = ctk.CTkFrame(master = self, height=100,width=750) #frame hosting buttons
        frame_button.grid(row = 2, column = 0, sticky = "nswe", padx=10, pady=10)
        frame_button.columnconfigure(0,weight = 1)
        frame_button.rowconfigure(0,weight = 1)
        frame_table = ctk.CTkFrame(master = self) #frame for listing tables
        frame_table.grid(row = 1, column = 0, sticky = "nswe", padx=10, pady=10)
        frame_table.columnconfigure(6,weight = 1)
        frame_table.rowconfigure(10,weight = 1)

        btn_new_req = ctk.CTkButton(master=frame_button, text = "Create New Request")
        btn_new_req.grid(row = 0, column = 0)
       
        #initialize table header
        lbl_id = ctk.CTkLabel(master = frame_table, text = "Request ID")
        lbl_id.grid(row = 0, column = 0)
        lbl_item = ctk.CTkLabel(master = frame_table, text = "Item")
        lbl_item.grid(row = 0, column = 1)
        lbl_qty = ctk.CTkLabel(master = frame_table, text = "Qty")
        lbl_qty.grid(row = 0, column = 2)
        lbl_client = ctk.CTkLabel(master = frame_table, text = "Generated By")
        lbl_client.grid(row = 0, column = 3)
        lbl_manager = ctk.CTkLabel(master = frame_table, text = "Assigned Manager")
        lbl_manager.grid(row = 0, column = 4)
        lbl_status = ctk.CTkLabel(master = frame_table, text = "Request Status")
        lbl_status.grid(row = 0, column = 5)
        
        for i in range (1, 11):
            for j in range (0,6):
                lblTemp = ctk.CTkLabel(master = frame_table, text = "chip")
                lblTemp.grid(row = i, column = j)
        
class RequestReviewPage(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)
        self.grid_columnconfigure(0,weight = 1)
        self.grid_rowconfigure(2,weight = 1)

        lbl_reqmanagement = ctk.CTkLabel(self, text="Request Review")
        lbl_reqmanagement.grid(row = 0, column = 0)

        #set Parent grid
        frame_bottom = ctk.CTkFrame(master = self, height=100,width=750) 
        frame_bottom.grid(row = 2, column = 0, sticky = "nswe", padx=10, pady=10)
        frame_bottom.columnconfigure(2,weight = 1)
        frame_bottom.rowconfigure(0,weight = 1)
        frame_table = ctk.CTkFrame(master = self) #frame for listing tables
        frame_table.grid(row = 1, column = 0, sticky = "nswe", padx=10, pady=10)
        frame_table.columnconfigure(6,weight = 1)
        frame_table.rowconfigure(10,weight = 1)
        
        #configure list for drop down list
        list = ['this','is','a','test']
        requestDropDown = ctk.CTkComboBox(master = frame_bottom, values = list)
        requestDropDown.set("Select a Request")
        requestDropDown.grid(row = 0, column = 0)

        #define buttons for acepting/rejecting requests
        accept_btn = ctk.CTkButton(master = frame_bottom, text = "Accept",text_color= "green")
        accept_btn.grid(row = 0, column = 1, padx = 15)
        reject_btn = ctk.CTkButton(master = frame_bottom, text = "Reject",text_color= "red")
        reject_btn.grid(row = 0, column = 2, padx = 15)

       #initialize table header
        lbl_id = ctk.CTkLabel(master = frame_table, text = "Request ID")
        lbl_id.grid(row = 0, column = 0)
        lbl_item = ctk.CTkLabel(master = frame_table, text = "Item")
        lbl_item.grid(row = 0, column = 1)
        lbl_qty = ctk.CTkLabel(master = frame_table, text = "Qty")
        lbl_qty.grid(row = 0, column = 2)
        lbl_client = ctk.CTkLabel(master = frame_table, text = "Generated By")
        lbl_client.grid(row = 0, column = 3)
        lbl_manager = ctk.CTkLabel(master = frame_table, text = "Assigned Manager")
        lbl_manager.grid(row = 0, column = 4)
        lbl_status = ctk.CTkLabel(master = frame_table, text = "Request Status")
        lbl_status.grid(row = 0, column = 5)
        
        for i in range (1, 11):
            for j in range (0,6):
                lblTemp = ctk.CTkLabel(master = frame_table, text = "chicken sandwich")
                lblTemp.grid(row = i, column = j)

class QuoteManagementPage(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)
        self.grid_columnconfigure(0,weight = 1)
        self.grid_rowconfigure(2,weight = 1)

        lbl_reqmanagement = ctk.CTkLabel(self, text="Quote Management")
        lbl_reqmanagement.grid(row = 0, column = 0)

        #set Parent grid
        frame_bottom = ctk.CTkFrame(master = self, height=100,width=750) #frame hosting buttons
        frame_bottom.grid(row = 2, column = 0, sticky = "nswe", padx=10, pady=10)
        frame_bottom.columnconfigure(1,weight = 1)
        frame_bottom.rowconfigure(1,weight = 1)
        frame_table = ctk.CTkFrame(master = self) #frame for listing tables
        frame_table.grid(row = 1, column = 0, sticky = "nswe", padx=10, pady=10)
        frame_table.columnconfigure(6,weight = 1)
        frame_table.rowconfigure(10,weight = 1)

        #configure list for drop down list
        list = ['this','is','a','test']
        requestDropDown = ctk.CTkComboBox(master = frame_bottom, values = list)
        requestDropDown.set("Select a Request")
        requestDropDown.grid(row = 0,column = 0, sticky = "w", pady = 15)

        priceTextField = ctk.CTkEntry(master = frame_bottom, width=100, placeholder_text="Quote Price")
        priceTextField.grid(row = 1, column = 1, sticky = "n", pady = 15)

        sendButton = ctk.CTkButton(master = frame_bottom,text = "Send Quote")
        sendButton.grid(row = 2, column = 2, sticky = "n", pady = 15)
       
        lbl_id = ctk.CTkLabel(master = frame_table, text = "Request ID")
        lbl_id.grid(row = 0, column = 0)
        lbl_item = ctk.CTkLabel(master = frame_table, text = "Item")
        lbl_item.grid(row = 0, column = 1)
        lbl_qty = ctk.CTkLabel(master = frame_table, text = "Qty")
        lbl_qty.grid(row = 0, column = 2)
        lbl_client = ctk.CTkLabel(master = frame_table, text = "Generated By")
        lbl_client.grid(row = 0, column = 3)
        lbl_manager = ctk.CTkLabel(master = frame_table, text = "Assigned Manager")
        lbl_manager.grid(row = 0, column = 4)
        lbl_status = ctk.CTkLabel(master = frame_table, text = "Request Status")
        lbl_status.grid(row = 0, column = 5)
        
        for i in range (1, 11):
            for j in range (0,6):
                lblTemp = ctk.CTkLabel(master = frame_table, text = "bacon")
                lblTemp.grid(row = i, column = j)

class SupplierManagementPage(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)
        self.grid_columnconfigure(0,weight = 1)
        self.grid_rowconfigure(2,weight = 1)

        lbl_reqmanagement = ctk.CTkLabel(self, text="Supplier Management")
        lbl_reqmanagement.grid(row = 0, column = 0)

        # #set Parent grid
        frame_button = ctk.CTkFrame(master = self, height=100,width=750) #frame hosting buttons
        frame_button.grid(row = 2, column = 0, sticky = "nswe", padx=10, pady=10)
        frame_button.columnconfigure(2,weight = 1)
        frame_button.rowconfigure(0,weight = 1)
        frame_table = ctk.CTkFrame(master = self) #frame for listing tables
        frame_table.grid(row = 1, column = 0, sticky = "nswe", padx=10, pady=10)
        frame_table.columnconfigure(1,weight = 1)
        frame_table.rowconfigure(10,weight = 1)

        btn_new_supplier = ctk.CTkButton(master=frame_button, text = "Add New Supplier")
        btn_new_supplier.grid(row = 0, column = 0)
        btn_add_item = ctk.CTkButton(master = frame_button, text = "Add New Item")
        btn_add_item. grid(row = 0, column = 1,sticky = "e")
       
        lbl_id = ctk.CTkLabel(master = frame_table, text = "Supplier")
        lbl_id.grid(row = 0, column = 0)
        lbl_item = ctk.CTkLabel(master = frame_table, text = "Items")
        lbl_item.grid(row = 0, column = 1)
     
        for i in range (1, 11):
            for j in range (0,2):
                lblTemp = ctk.CTkLabel(master = frame_table, text = "pizza")
                lblTemp.grid(row = i, column = j)

def load_image(path, image_size):
        """ Load image """
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size, image_size)))

