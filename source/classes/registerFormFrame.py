import tkinter as tk
import customtkinter as ctk

from source.utils import add_patient, username_exists
from source.classes.customWidgets.intSpinbox import IntSpinbox


class RegisterFormFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        
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
        problem_teeth_count = self.teeth_count_spinbox.get()

        default_color = ("#979DA2", "#565B5E")

        entrys = [self.username_entry, self.password_entry, self.confirm_password_entry,
                  self.insurance_combobox, self.dental_problem_combobox]

        entry_map = [
            [self.username_entry, username == "", "no username given"],
            [self.password_entry, password == "", "no password given"],
            [self.confirm_password_entry, confirm_password == "", "confirm your password"],
            [self.confirm_password_entry, confirm_password != password, "your confirmation password does not match"],
            [self.insurance_combobox, insurance == "Krankenkassenart", "choose your type of insurance"],
            [self.dental_problem_combobox, dental_problem == "Dentale Problematik", "choose your dental problem"],
            [self.username_entry, username_exists(username), "username already exists"]]

        error_entrys = []
        for entry, is_problem, error_string in entry_map:
            if is_problem:
                error_entrys.append(entry)
                print(error_string)

        for entry in entrys:
            entry.configure(border_color=("red" if entry in error_entrys else default_color))

        if error_entrys:  # not empty
            return

        add_patient({
            "username": username,
            "password": password,
            "insurance": insurance,
            "dental_problem": dental_problem,
            "problem_teeth_count": problem_teeth_count
        })
        print("patient added")
        self.master.grid_forget()
        self.nametowidget(".").login_sidebar.grid_forget()
        self.nametowidget(".").main_grid(username)
        