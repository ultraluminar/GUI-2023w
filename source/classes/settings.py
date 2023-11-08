import customtkinter as ctk

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("480x400")
        self.title("Einstellungen")
        self.resizable(False, False)

        self.font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        self.font20 = ctk.CTkFont(family="Segoe UI", size=20, weight="bold")
        
        self.main_label = ctk.CTkLabel(self, text="Einstellungen", font=self.font24)

        # design subframe
        self.design_frame = ctk.CTkFrame(self)
        self.design_label = ctk.CTkLabel(self.design_frame, text="Farbdesign ändern", font=self.font20)
        self.design_frame_placeholder = ctk.CTkLabel(self.design_frame, text="")
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.design_frame, values=["Light", "Dark", "System"],
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.set("System")
        
        # password change subframe
        self.change_password_frame = ctk.CTkFrame(self)
        self.change_password_label = ctk.CTkLabel(self.change_password_frame, text="Passwort ändern", font=self.font20)
        self.password_frame_placeholder = ctk.CTkLabel(self.change_password_frame, text="")
        self.old_password_entry = ctk.CTkEntry(self.change_password_frame, placeholder_text="Altes Passwort")
        self.new_passwort_entry = ctk.CTkEntry(self.change_password_frame, placeholder_text="Neues Passwort")
        self.change_password_button = ctk.CTkButton(self.change_password_frame, text="Passwort ändern")
                
        self.design_label.grid(row=0, column=0, padx=20, pady=(15, 20))
        self.design_frame_placeholder.grid(row=0, column=1, ipadx=142)
        self.appearance_mode_optionemenu.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        self.change_password_label.grid(row=0, column=0, padx=20, pady=(15, 20))
        self.password_frame_placeholder.grid(row=0, column=1, ipadx=154)
        self.old_password_entry.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        self.new_passwort_entry.grid(row=2, column=0, columnspan=2, pady=(0, 20))
        self.change_password_button.grid(row=3, column=0, columnspan=2, pady=(0, 20))
        
        self.main_label.pack(pady=(10, 15))
        self.design_frame.pack(pady=(0, 15))
        self.change_password_frame.pack()
        
    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        