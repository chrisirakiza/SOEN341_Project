import customtkinter as ctk # pip install customtkinter
import GUIData
import GUIFrames
import System

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')


class ProcSysGUI(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.sys = System.ProcurementSystem()
        self.gui_data = GUIData.GUIData()

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
        self.active_page = GUIFrames.PageTypes.PLACEHOLDER
        self.pageDict[self.active_page].grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
    
    def DisplayPage(self, pagetype):
        if pagetype == self.active_page:
            return

        for key, page in self.pageDict.items():
            page.grid_forget()
        
        newpage = self.pageDict[pagetype]
        newpage.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.active_page = pagetype

    def Login(self, userID, password):
        print(f"U: {userID}, P:{password}")
        self.sys.SwitchActiveUser(userID, password)
        self.UpdateActiveUser()
    
    def UpdateActiveUser(self) -> None:
        name, userID, pwd, userType = self.sys.GetUserValues(self.sys.active_user)
        self.gui_data.active_user_data["name"].set(name.replace("_", " "))
        self.gui_data.active_user_data["id"].set(userID)
        self.gui_data.active_user_data["type"].set(userType)


if __name__ == "__main__":
    app = ProcSysGUI()
    app.mainloop()
