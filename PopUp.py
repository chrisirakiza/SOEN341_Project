import customtkinter as ctk # pip install customtkinter

def popupError(e) -> None:
    '''Creates a popup window for an error'''
    # Create window
    popupErrorWindow = ctk.CTkToplevel()
    popupErrorWindow.wm_title("Error")
    popupErrorWindow.configure(height = 20, width = 40)
    # Populate window
    labelError = ctk.CTkLabel(popupErrorWindow, text = str(e) + "!")
    labelError.grid(row=0, column=0,pady = 10)
    closeButton = ctk.CTkButton(master = popupErrorWindow, text="OK", command=lambda: popupErrorWindow.destroy())
    closeButton.grid(row=1,column = 0, pady = 10)

def popupMessage(m) -> None:
    '''Creates a popup window for Messages'''
    # Create window
    popupMessageWindow = ctk.CTkToplevel()
    popupMessageWindow.wm_title("Message")
    popupMessageWindow.configure(height = 20, width = 40)
    # Populate window
    labelError = ctk.CTkLabel(popupMessageWindow, text = str(m) + "!")
    labelError.grid(row=0, column=0,pady = 10)
    closeButton = ctk.CTkButton(master = popupMessageWindow, text="OK", command=lambda: popupMessageWindow.destroy())
    closeButton.grid(row=1,column = 0, pady = 10)