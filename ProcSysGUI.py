import customtkinter as ctk # pip install customtkinter
import GUIData
import GUIFrames
import System

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

def popupError(e):       #basic exception handling popup window
    popupErrorWindow = ctk.CTkToplevel()
    popupErrorWindow.wm_title("Error")
    popupErrorWindow.config(height = 20, width = 40)
    labelError = ctk.CTkLabel(popupErrorWindow, text = str(e) + "!")
    labelError.grid(row=0, column=0,pady = 10)
    closeButton = ctk.CTkButton(master = popupErrorWindow, text="OK", command=lambda: popupErrorWindow.destroy())
    closeButton.grid(row=1,column = 0, pady = 10)

class ProcSysGUI(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.sys = System.ProcurementSystem()
        self.gui_data = GUIData.GUIData()
        self.gui_data.UpdateUserData(self.sys)

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
        self.active_page = GUIFrames.PageTypes.PLACEHOLDER #can be changed for debugging
        self.pageDict[self.active_page].grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
    
    def DisplayPage(self, pagetype):
        if pagetype == self.active_page:
            return

        for key, page in self.pageDict.items():
            page.grid_forget()
        
        newpage = self.pageDict[pagetype]
        newpage.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        newpage.LoadPage()
        self.active_page = pagetype

    def Login(self, userID, password):
        print(f"U: {userID}, P:{password}")
        try:
            self.sys.SwitchActiveUser(userID, password)
            self.UpdateActiveUser()
            self.DisplayPage(GUIFrames.PageTypes.PLACEHOLDER)
        except Exception as e:
            popupError(e)

    
    def UpdateActiveUser(self) -> None:
        name, userID, pwd, userType = self.sys.GetUserValues(self.sys.active_user)
        self.gui_data.active_user_data["name"].set(name.replace("_", " "))
        self.gui_data.active_user_data["id"].set(userID)
        self.gui_data.active_user_data["type"].set(userType)

    def CreateUser(self, userType, username, pwd):
        if (username == ""):
            popupError("Username required")
            return
        if (pwd == ""):
            popupError("Password required")
            return
        self.sys.CreateNewUser(userType, username.replace(" ", "_"), pwd)
        self.gui_data.UpdateUserData(self.sys)
        self.DisplayPage(GUIFrames.PageTypes.USER_MANAGEMENT)


if __name__ == "__main__": 
    app = ProcSysGUI()
    app.mainloop()
