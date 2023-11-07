from typing import Optional, Tuple, Union
import customtkinter as ctk

# variables
sidebar_width = 140

class LoginSidebar(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk):
        super().__init__(master=master, width=sidebar_width, corner_radius=0)

        self.grid_rowconfigure(1, weight=1)
        
        self.logo_label = ctk.CTkLabel(self, text="Dental Manager", font=ctk.CTkFont(size=20, weight="bold"))
        self.exit_button = ctk.CTkButton(self, text="Beenden", command=exit)
        
        self.set_grid()
    
    def set_grid(self):
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.exit_button.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="s")
        
    def exit(self):
        self.master.exit()
