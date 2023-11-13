import customtkinter as ctk

from source.utils import username_exists, check_login, update_password

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, username: str):
        super().__init__()
        self.geometry("480x400")
        self.title("Einstellungen")
        self.resizable(False, False)
        
        self.username = username 

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
        self.old_password_entry = ctk.CTkEntry(self.change_password_frame, placeholder_text="Altes Passwort", show="•")
        self.new_passwort_entry = ctk.CTkEntry(self.change_password_frame, placeholder_text="Neues Passwort", show="•")
        self.change_password_button = ctk.CTkButton(self.change_password_frame, text="Passwort ändern", command=self.change_password)
                
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
        
        self.bind("<Return>", self.change_password)
        
    def change_appearance_mode_event(self, new_appearance_mode: str):
        if new_appearance_mode.lower() != ctk.get_appearance_mode():
            ctk.set_appearance_mode(new_appearance_mode)
            #TODO add focus lose fix
        
    def change_password(self, event=None):
        default_color = ("#979DA2", "#565B5E")
        
        if not check_login(username=self.username, password=self.old_password_entry.get()):
            self.old_password_entry.configure(border_color="red")
            print("Password is incorrect")
            return
        else:
            self.old_password_entry.configure(border_color=default_color)
        if self.new_passwort_entry.get() == "":
            self.new_passwort_entry.configure(border_color="red")
            print("please give a new password")
            return
        else:
            self.new_passwort_entry.configure(border_color=default_color)
        update_password(username=self.username, password=self.new_passwort_entry.get())
        self.old_password_entry.configure(border_color="green")
        self.new_passwort_entry.configure(border_color="green")
        print("password changed")
