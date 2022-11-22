import customtkinter as ctk # pip install customtkinter

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

class Page(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        ctk.CTkFrame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class NavigationBar(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.grid_columnconfigure(0, weight=1)  
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkFrame(master=self, height=100).grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
        NavBar_User(master=self).grid(row=1, column=0, sticky="nswe", padx=10, pady=10)


class NavBar_User(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        btn_userManagement = ctk.CTkButton(master=self, text="User")
        btn_requestManagement = ctk.CTkButton(master=self, text="Requests")
        btn_userManagement.pack(side="top", fill="both", expand=False, padx=10, pady=10)
        btn_requestManagement.pack(side="top", fill="both", expand=False, padx=10, pady=10)


class UserManagementPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ctk.CTkLabel(self, text="This is user management")
        label.pack(side="top", fill="both", expand=True)

class RequestSystemPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = ctk.CTkLabel(self, text="This is request management")
        label.pack(side="top", fill="both", expand=True)

class ProcSysGUI(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Procurement System Prototype")
        self.geometry("800x600")
        # create two frames

        self.page_dict = {}

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        navigation_bar = NavigationBar(master=self, width=180, corner_radius=0)
        self.page_dict["navigation_bar"] = navigation_bar
        navigation_bar.grid(row=0, column=0, sticky="nswe")

        user_management_page = UserManagementPage(master=self)
        self.page_dict["user_management_page"] = user_management_page
        request_page = RequestSystemPage(master=self)
        self.page_dict["request_page"] = request_page
        # self.user_management_page.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # Configure navigation bar
    
    def SwapMenu(self, menu):
        pass


if __name__ == "__main__":
    app = ProcSysGUI()
    app.mainloop()
