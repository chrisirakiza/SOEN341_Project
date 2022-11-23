import customtkinter as ctk

class GUIData():
    def __init__(self):
        self.active_user_data = {
            "name": ctk.StringVar(),
            "id": ctk.StringVar(),
            "type": ctk.StringVar()
        }