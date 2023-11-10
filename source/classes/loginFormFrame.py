import customtkinter as ctk
from source.utils import username_exists, check_login

class LoginFormFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        self.font15 = ctk.CTkFont(family="Segoe UI", size=15)
        # self.font13 = ctk.CTkFont(family="Segoe UI", size=13)

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

        if username == "":
            self.username_entry.configure(border_color="red")
            print("please give a username")
            return
        else: 
            self.username_entry.configure(border_color=default_color)
        if not username_exists(username):
            self.username_entry.configure(border_color="red")
            print("username doesn't exist")
            return
        else: 
            self.username_entry.configure(border_color=default_color)
        if password == "":
            self.password_entry.configure(border_color="red")
            print("please give a password")
            return
        else:
            self.password_entry.configure(border_color=default_color)
        if check_login(username, password):
            print("logged in")
            self.master.grid_forget()
            self.nametowidget(".").login_sidebar.grid_forget()
            self.nametowidget(".").main_grid(username)
        else:
            self.password_entry.configure(border_color="red")
            print("password incorrect")