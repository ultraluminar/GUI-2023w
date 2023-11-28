import customtkinter as ctk

class Main(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk):
        super().__init__(master=master, corner_radius=0, fg_color="transparent")
        
        self.auth_service = self.nametowidget(".").auth_service
        
        self.label = ctk.CTkLabel(self)
        self.label.pack()
        
    def grid(self, *args, **kwargs):
        self.label.configure(text=f"logged in as {self.auth_service.username}")
        super().grid(*args, **kwargs)