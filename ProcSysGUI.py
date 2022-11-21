import customtkinter as ctk # pip install customtkinter

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

class NavigationBar(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        ctk.CTkFrame.__init__(self, *args, **kwargs)
        self.button = ctk.CTkButton(master=self, text="Button")
        self.button.pack(side="top", fill="both", expand=False, pady=10, padx=10)

    def show(self):
        self.lift()

class Page(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        ctk.CTkFrame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

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

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.navigation_bar = NavigationBar(master=self, width=180, corner_radius=0)
        self.navigation_bar.grid(row=0, column=0, sticky="nswe")

        self.user_management_page = RequestSystemPage(master=self)
        self.user_management_page.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # Configure navigation bar


if __name__ == "__main__":
    app = ProcSysGUI()
    app.mainloop()
