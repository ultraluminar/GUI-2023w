import customtkinter as ctk
from source.classes.settings import SettingsWindow

sidebar_width = 140

class MainSidebar(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk, username: str):
        super().__init__(master=master, width=sidebar_width, corner_radius=0)
        self.username = username
        
        self.grid_rowconfigure(1, weight=1)
        
        # widgets
        self.logo_label = ctk.CTkLabel(self, text="Dental Manager", font=ctk.CTkFont(size=20, weight="bold"))
        self.settings_button = ctk.CTkButton(self, text="Einstellungen", command=self.settings)
        self.settings_window = None
        self.logout_button = ctk.CTkButton(self, text="Abmelden", command=self.logout)
        
        self.set_grid()
        
    def set_grid(self):
        self.logo_label.grid(row=0, column=0, padx=15, pady=(20, 10))
        self.settings_button.grid(row=2, column=0, padx=15, pady=(0, 15))
        self.logout_button.grid(row=3, column=0, padx=15, pady=(0, 20))
        
    def settings(self):
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow(username=self.username)     # create window if its None or destroyed
        elif self.settings_window.state() == "iconic":
            self.settings_window.deiconify()    # bring back window if its minimized
        else:
            self.settings_window.focus()
    
    # hides widgets from the main view and brings back login widgets
    def logout(self):
        self.grid_forget()
        self.nametowidget(".").main_main.grid_forget()
        self.nametowidget(".").initial_grid()
        