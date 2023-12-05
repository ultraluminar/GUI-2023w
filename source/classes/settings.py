import customtkinter as ctk

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        
        #variables
        settings_width = 440
        settings_height = 400
        
        # initialize window
        self.geometry(f"{settings_width}x{settings_height}")
        self.title("Einstellungen")
        self.resizable(False, False)
        
        self.auth_service = self.nametowidget(".").auth_service

        # fonts
        self.font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        self.font20 = ctk.CTkFont(family="Segoe UI", size=20, weight="bold")
        
        # widgets
        self.main_label = ctk.CTkLabel(self, text="Einstellungen", font=self.font24)

        # design subframe widgets
        self.design_frame = ctk.CTkFrame(self)
        self.design_label = ctk.CTkLabel(self.design_frame, text="Farbdesign ändern", font=self.font20)
        self.design_frame_placeholder = ctk.CTkLabel(self.design_frame, text="")
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.design_frame, values=["Light", "Dark", "System"],
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.set("System")
        
        # password change subframe widgets
        self.change_password_frame = ctk.CTkFrame(self)
        self.change_password_label = ctk.CTkLabel(self.change_password_frame, text="Passwort ändern", font=self.font20)
        self.password_frame_placeholder = ctk.CTkLabel(self.change_password_frame, text="")
        self.old_password_entry = ctk.CTkEntry(self.change_password_frame, placeholder_text="Altes Passwort", show="•")
        self.new_password_entry = ctk.CTkEntry(self.change_password_frame, placeholder_text="Neues Passwort", show="•")
        self.change_password_button = ctk.CTkButton(self.change_password_frame, text="Passwort ändern", command=self.change_password)
        
        # design subframe grid       
        self.design_label.grid(row=0, column=0, padx=20, pady=(15, 20))
        self.design_frame_placeholder.grid(row=0, column=1, ipadx=138)
        self.appearance_mode_optionemenu.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # password change subframe grid
        self.change_password_label.grid(row=0, column=0, padx=20, pady=(15, 20))
        self.password_frame_placeholder.grid(row=0, column=1, ipadx=154)
        self.old_password_entry.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        self.new_password_entry.grid(row=2, column=0, columnspan=2, pady=(0, 20))
        self.change_password_button.grid(row=3, column=0, columnspan=2, pady=(0, 20))
        
        # main label and subframe packing on window
        self.main_label.pack(pady=(10, 15))
        self.design_frame.pack(pady=(0, 15))
        self.change_password_frame.pack()
        
        # binging Return Key to password changing function
        self.bind("<Return>", self.change_password)
        
    def change_appearance_mode_event(self, new_appearance_mode: str):
        current = ctk.get_appearance_mode()
        if current != "System" and new_appearance_mode != current:
            ctk.set_appearance_mode(new_appearance_mode)
            self.after(1, self.lift)

        
    def change_password(self, event=None):
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()

        default_color = ("#979DA2", "#565B5E")

        entrys = [self.old_password_entry, self.new_password_entry]

        entry_map = [
            [self.old_password_entry, old_password == "", "please enter ure old password"],
            [self.old_password_entry, not self.auth_service.check_login(self.auth_service.username, old_password), "Password is incorrect"],
            [self.new_password_entry, new_password == "", "please give a new password"],
            [self.new_password_entry, old_password == new_password, "password has not changed"]
        ]

        error_entrys = []
        for entry, is_problem, error_string in entry_map:
            if is_problem:
                error_entrys.append(entry)
                print(error_string)
                break

        for entry in entrys:
            entry.configure(border_color=("red" if entry in error_entrys else default_color))

        if error_entrys:  # not empty:
            return

        self.auth_service.update_password(new_password=new_password)
        self.old_password_entry.configure(border_color="green")
        self.new_password_entry.configure(border_color="green")
        print("password changed")