import customtkinter as ctk
from test.utils import mcheck

class LoginFormFrame(ctk.CTkFrame):
    def __init__(self, master, pwds: dict):
        super().__init__(master=master)
        self.pwds = pwds
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

        if username == "":
            self.username_entry.configure(border_color="red")
            print("please give a username")
            return
        else: 
            self.username_entry.configure(border_color=("#979DA2", "#565B5E"))
        if username not in self.pwds.keys():
            self.username_entry.configure(border_color="red")
            print("username doesn't exist")
            return
        else: 
            self.username_entry.configure(border_color=("#979DA2", "#565B5E"))
        if password == "":
            self.password_entry.configure(border_color="red")
            print("please give a password")
            return
        else:
            self.password_entry.configure(border_color=("#979DA2", "#565B5E"))
        if mcheck(password, self.pwds[username]):
            print("logged in")
        else:
            self.password_entry.configure(border_color="red")
            print("password incorrect")