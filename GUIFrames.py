import customtkinter as ctk
from enum import Enum
from PIL import Image, ImageTk
import os

PATH = os.path.dirname(os.path.realpath(__file__))

class PageTypes(Enum):
    PLACEHOLDER = 0
    LOGIN = 1

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

        # User info
        name, userID, pwd, userType = self.root.sys.GetUserValues(self.root.sys.active_user)
        lbl_username = ctk.CTkLabel(self, text=f"User: {name}\nID: {userID}")
        lbl_username.grid(row=0, column=1)

class NavBar_Selector(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

class LoginPage(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        lbl_placeholder = ctk.CTkLabel(self, text="Login")
        lbl_placeholder.pack()

class PlaceHolderPage(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        lbl_placeholder = ctk.CTkLabel(self, text="Placeholder")
        lbl_placeholder.pack()


def load_image(path, image_size):
        """ Load image """
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size, image_size)))

# class NavigationBar(Page):
#     def __init__(self, root, *args, **kwargs):
#         Page.__init__(self, *args, **kwargs)
#         self.gui = root
#         self.gui.CoolFunc()
#         self.grid_columnconfigure(0, weight=1)  
#         self.grid_rowconfigure(1, weight=1)

#         LoginScreen(master=self, height=100).grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
#         NavBar_User(master=self).grid(row=1, column=0, sticky="nswe", padx=10, pady=10)


# class NavBar_User(Page):
#     def __init__(self, *args, **kwargs):
#         Page.__init__(self, *args, **kwargs)

#         btn_userManagement = ctk.CTkButton(master=self, text="User")
#         btn_requestManagement = ctk.CTkButton(master=self, text="Requests")
#         btn_userManagement.pack(side="top", fill="both", expand=False, padx=1, pady=5)
#         btn_requestManagement.pack(side="top", fill="both", expand=False, padx=1, pady=5)


# class UserManagementPage(Page):
#     def __init__(self, *args, **kwargs):
#         Page.__init__(self, *args, **kwargs)
#         label = ctk.CTkLabel(self, text="This is user management")
#         label.pack(side="top", fill="both", expand=True)

# class RequestSystemPage(Page):
#     def __init__(self, *args, **kwargs):
#         Page.__init__(self, *args, **kwargs)
#         label = ctk.CTkLabel(self, text="This is request management")
#         label.pack(side="top", fill="both", expand=True)

# class LoginScreen(Page):
#     def __init__(self, *args, **kwargs):
#         Page.__init__(self, *args, **kwargs)
#         self.icon = ImageTk.PhotoImage(Image.open("C:/Users/zacha/Desktop/School/SOEN341/SOEN341-Project/SOEN341_Project/user.png").resize((20,20)))
#         ctk.CTkButton(master=self, image=self.icon, text="Test", fg_color=("black", "black")).pack()