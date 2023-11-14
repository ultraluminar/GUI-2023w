import customtkinter as ctk

class LoginFormFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.font15 = ctk.CTkFont(family="Segoe UI", size=15)
        # self.font13 = ctk.CTkFont(family="Segoe UI", size=13)

        self.auth_service = self.nametowidget(".").auth_service

        self.heading = ctk.CTkLabel(master=self, font=self.font15, text="Bitte melden sie sich an")
        self.username_entry = ctk.CTkEntry(self, width=160, placeholder_text="Benutzername")
        self.password_entry = ctk.CTkEntry(self, width=160, placeholder_text="Passwort", show="•")
        self.login_button = ctk.CTkButton(self, text="Einloggen", command=self.try_login)

        self.set_grid()

    def set_grid(self):
        self.heading.grid(row=1, column=0, pady=(20, 0), padx=0, sticky="n")
        self.username_entry.grid(row=2, column=0, pady=(20, 0), padx=50, sticky="n")
        self.password_entry.grid(row=3, column=0, pady=(15, 0), padx=50, sticky="n")
        self.login_button.grid(row=4, column=0, pady=(25, 30), padx=50, sticky="n")

    def try_login(self, event=None) -> None:
        username = self.username_entry.get()
        password = self.password_entry.get()
        default_color = ("#979DA2", "#565B5E")

        entrys = [self.username_entry, self.password_entry]

        entry_map = [
            [self.username_entry, username == "", "please give a username"],
            [self.username_entry, not self.auth_service.username_exists(username), "username doesn't exist"],
            [self.password_entry, password == "", "please give a password"],
            [self.password_entry, not self.auth_service.check_login(username, password), "password incorrect"]
        ]

        error_entrys = []
        for entry, is_problem, error_string in entry_map:
            if is_problem:
                error_entrys.append(entry)
                print(error_string)
                break  # to prevent seeing errors like "username doesn't exist" on empty username

        for entry in entrys:
            entry.configure(border_color=("red" if entry in error_entrys else default_color))

        if error_entrys:  # not empty
            return

        print("logged in")
        self.password_entry.delete(0, "end")   # deletes the password entry for privacy
        self.nametowidget(".!ctkframe.!canvas.!mainloginframe").grid_forget()
        self.nametowidget(".").login_sidebar.grid_forget()
        self.nametowidget(".").main_grid(username)
