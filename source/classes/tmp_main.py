import customtkinter as ctk

class Main(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk):
        super().__init__(master=master, corner_radius=0, fg_color="transparent")
        
        self.label = ctk.CTkLabel(self, text="logged in")
        self.label.pack()