import tkinter as tk
import customtkinter as ctk

from json import dump
from source.utils import mhash
from source.classes.customWidgets.intSpinbox import IntSpinbox


class RegisterFormFrame(ctk.CTkFrame):
    def __init__(self, master, pwds: dict):
        super().__init__(master=master)

        self.pwds = pwds
        self.input_width = 160

        self.font15 = ctk.CTkFont(family="Segoe UI", size=15)

        self.insurance_var = tk.StringVar(value="Krankenkassenart")
        self.dental_problem_var = tk.StringVar(value="Dentale Problematik")
        self.teeth_count_string = tk.StringVar(value="Anzahl zu behandelnder Zähne")
        self.teeth_count_var = tk.IntVar()

        self.insurance_types = ["gesetzlich", "freiwillig gesetzlich", "privat"]
        self.dental_problem_types = ["Karies klein", "Karies groß", "Teilkrone", "Krone", "Wurzelbehandlung"]

        self.heading = ctk.CTkLabel(self, font=self.font15, text="Bitte hier registrieren")
        self.username_entry = ctk.CTkEntry(self, width=self.input_width, placeholder_text="Benutzername")
        self.password_entry = ctk.CTkEntry(self, width=self.input_width, placeholder_text="Passwort", show="•")
        self.confirm_password_entry = ctk.CTkEntry(self, width=self.input_width, placeholder_text="Passwort bestätigen", show="•")

        self.insurance_combobox = ctk.CTkComboBox(
            self, width=self.input_width, values=self.insurance_types, variable=self.insurance_var, state="readonly")
        self.dental_problem_combobox = ctk.CTkComboBox(
            self, width=self.input_width, values=self.dental_problem_types, variable=self.dental_problem_var, state="readonly")

        self.teeth_count_spinbox = IntSpinbox(self, width=self.input_width)
        self.register_button = ctk.CTkButton(self, text="Registrieren", command=self.try_register)

        self.set_grid()

    def set_grid(self):
        self.heading.grid(row=1, column=0, pady=(20, 0), padx=0, sticky="n")
        self.username_entry.grid(row=2, column=0, pady=(20, 0), padx=50, sticky="n")
        self.password_entry.grid(row=3, column=0, pady=(15, 0), padx=50, sticky="n")
        self.confirm_password_entry.grid(row=4, column=0, pady=(10, 0), padx=50, sticky="n")
        self.insurance_combobox.grid(row=5, column=0, pady=(15, 0), padx=50, sticky="n")
        self.dental_problem_combobox.grid(row=6, column=0, pady=(15, 0), padx=50, sticky="n")
        self.teeth_count_spinbox.grid(row=7, column=0, pady=(15, 0), padx=50, sticky="n")
        self.register_button.grid(row=8, column=0, pady=(25, 30), padx=50, sticky="n")

    def try_register(self, event=None) -> None:
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        insurance = self.insurance_var.get()
        dental_problem = self.dental_problem_var.get()

        if username == "":
            print("no username given")
            self.username_entry.configure(border_color = "red")
            return
        else:
            self.username_entry.configure(border_color=("#979DA2", "#565B5E"))
        if password == "":
            print("no password given")
            self.password_entry.configure(border_color = "red")
            return
        else:
            self.password_entry.configure(border_color=("#979DA2", "#565B5E"))
        if confirm_password == "":
            print("confirm your password")
            self.confirm_password_entry.configure(border_color = "red")
            return
        if not confirm_password == password:
            print("your confirmation password does not match")
            self.confirm_password_entry.configure(border_color = "red")
            return
        else:
            self.confirm_password_entry.configure(border_color=("#979DA2", "#565B5E"))
        if insurance == "Krankenkassenart":
            print("choose your type of insurance")
            print(self.insurance_combobox.cget("border_color"))
            self.insurance_combobox.configure(border_color = "red")
            return
        else:
            self.insurance_combobox.configure(border_color=("#979DA2", "#565B5E"))
        if dental_problem == "Dentale Problematik":
            print("choose your dental problem")
            self.dental_problem_combobox.configure(border_color = "red")
            return
        else:
            self.dental_problem_combobox.configure(border_color=("#979DA2", "#565B5E"))
        if username in self.pwds.keys():
            print("username already exists")
            self.username_entry.configure(border_color = "red")
            return
        else:
            self.username_entry.configure(border_color=("#979DA2", "#565B5E"))
        

        self.pwds[username] = mhash(password)

        with open("test/pwd.json", mode="w") as filestream:
            dump(self.pwds, filestream, indent=4)
            