import tkinter as tk
import customtkinter as ctk

from source.classes.customWidgets.intSpinbox import IntSpinbox


class RegisterFormFrame(ctk.CTkTabview):
    def __init__(self, master):
        super().__init__(master=master)
        
        # tabs
        self.add("als Patient")
        self.add("als Zahnarzt")
        
        # variables
        self.input_width = 200
        self.auth_service = self.nametowidget(".").auth_service

        # font
        self.font15 = ctk.CTkFont(family="Segoe UI", size=15)

        # tk variables
        self.male = tk.BooleanVar(value=1)
        # patient tab
        self.insurance_var = tk.StringVar(value="Krankenkassenart")
        self.dental_problem_var = tk.StringVar(value="Dentale Problematik")
        self.teeth_count_var = tk.IntVar()

        self.insurance_types = ["gesetzlich", "freiwillig gesetzlich", "privat"]
        self.dental_problem_types = ["Karies klein", "Karies groß", "Teilkrone", "Krone", "Wurzelbehandlung"]
        # doctor tab
        self.insurance_private = tk.BooleanVar(value=False)
        self.insurance_by_law = tk.BooleanVar(value=False)
        self.insurance_voluntarily = tk.BooleanVar(value=False)

        # widgets
        # patient tab
        self.patient_heading = ctk.CTkLabel(self.tab("als Patient"), font=self.font15, text="Bitte hier registrieren")
        self.patient_username_entry = ctk.CTkEntry(self.tab("als Patient"), width=self.input_width, placeholder_text="Benutzername")
        self.patient_name_entry = ctk.CTkEntry(self.tab("als Patient"), width=self.input_width, placeholder_text="Name")
        self.patient_password_entry = ctk.CTkEntry(self.tab("als Patient"), width=self.input_width, placeholder_text="Passwort", show="•")
        self.patient_confirm_password_entry = ctk.CTkEntry(self.tab("als Patient"), width=self.input_width, placeholder_text="Passwort bestätigen", show="•")
        
        self.patient_adress_male = ctk.CTkRadioButton(self.tab("als Patient"), text="Herr", value=True, variable=self.male)
        self.patient_adress_female = ctk.CTkRadioButton(self.tab("als Patient"), text="Frau", value=False, variable=self.male)

        self.insurance_combobox = ctk.CTkComboBox(
            self.tab("als Patient"), width=self.input_width, values=self.insurance_types, variable=self.insurance_var, state="readonly")
        self.dental_problem_combobox = ctk.CTkComboBox(
            self.tab("als Patient"), width=self.input_width, values=self.dental_problem_types, variable=self.dental_problem_var, state="readonly")

        self.teeth_count_label = ctk.CTkLabel(self.tab("als Patient"), text="Anzahl zu behandelnder Zähne")
        self.teeth_count_spinbox = IntSpinbox(self.tab("als Patient"), width=self.input_width)
        self.patient_register_button = ctk.CTkButton(self.tab("als Patient"), text="Registrieren", command=self.try_patient_register)
        # doctor tab
        self.doctor_heading = ctk.CTkLabel(self.tab("als Zahnarzt"), font=self.font15, text="Bitte hier registrieren")
        self.doctor_username_entry = ctk.CTkEntry(self.tab("als Zahnarzt"), width=self.input_width, placeholder_text="Benutzername")
        self.doctor_name_entry = ctk.CTkEntry(self.tab("als Zahnarzt"), width=self.input_width, placeholder_text="Name")
        self.doctor_password_entry = ctk.CTkEntry(self.tab("als Zahnarzt"), width=self.input_width, placeholder_text="Passwort", show="•")
        self.doctor_confirm_password_entry = ctk.CTkEntry(self.tab("als Zahnarzt"), width=self.input_width, placeholder_text="Passwort bestätigen", show="•")
        
        self.doctor_adress_male = ctk.CTkRadioButton(self.tab("als Zahnarzt"), text="Herr", value=True, variable=self.male)
        self.doctor_adress_female = ctk.CTkRadioButton(self.tab("als Zahnarzt"), text="Frau", value=False, variable=self.male)

        self.doctor_insurance_label = ctk.CTkLabel(self.tab("als Zahnarzt"), text="Welche Patienten behandeln Sie?")
        self.doctor_insurance_checkbox_private = ctk.CTkCheckBox(self.tab("als Zahnarzt"), text="Privatversicherte", variable=self.insurance_private)
        self.doctor_insurance_checkbox_by_law = ctk.CTkCheckBox(self.tab("als Zahnarzt"), text="Gesetzlichversicherte", variable=self.insurance_by_law)
        self.doctor_insurance_checkbox_voluntarily = ctk.CTkCheckBox(self.tab("als Zahnarzt"), text="freiwillig Gesetzlichversicherte", variable=self.insurance_voluntarily)
        
        self.doctor_register_button = ctk.CTkButton(self.tab("als Zahnarzt"), text="Registrieren", command=self.try_doctor_register)
        
        # gridding
        self.set_patient_grid()
        self.set_doctor_grid()

    def set_patient_grid(self):
        self.patient_heading.grid(row=1, column=0, columnspan=2, pady=(10, 0), padx=0, sticky="n")
        self.patient_username_entry.grid(row=2, column=0, columnspan=2, pady=(20, 0), padx=50, sticky="n")
        self.patient_name_entry.grid(row=3, column=0, columnspan=2, pady=(10, 0), padx=50, sticky="n")
        self.patient_password_entry.grid(row=4, column=0, columnspan=2, pady=(15, 0), padx=50, sticky="n")
        self.patient_confirm_password_entry.grid(row=5, column=0, columnspan=2, pady=(10, 0), padx=50, sticky="n")
        self.patient_adress_male.grid(row=6, column=0, pady=(20, 0), padx=(70, 0), sticky="n")
        self.patient_adress_female.grid(row=6, column=1, pady=(20, 0), padx=(0, 30), sticky="n")
        self.insurance_combobox.grid(row=7, column=0, columnspan=2, pady=(15, 0), padx=50, sticky="n")
        self.dental_problem_combobox.grid(row=8, column=0, columnspan=2, pady=(15, 0), padx=50, sticky="n")
        self.teeth_count_label.grid(row=9, column=0, columnspan=2, pady=(10, 0), padx=50, sticky="n")
        self.teeth_count_spinbox.grid(row=10, column=0, columnspan=2, pady=(2, 0), padx=50, sticky="n")
        self.patient_register_button.grid(row=11, column=0, columnspan=2, pady=(25, 20), padx=50, sticky="n")
        
    def set_doctor_grid(self):
        self.doctor_heading.grid(row=1, column=0, columnspan=2, pady=(10, 0), padx=0, sticky="n")
        self.doctor_username_entry.grid(row=2, column=0, columnspan=2, pady=(20, 0), padx=50, sticky="n")
        self.doctor_name_entry.grid(row=3, column=0, columnspan=2, pady=(10, 0), padx=50, sticky="n")
        self.doctor_password_entry.grid(row=4, column=0, columnspan=2, pady=(15, 0), padx=50, sticky="n")
        self.doctor_confirm_password_entry.grid(row=5, column=0, columnspan=2, pady=(10, 0), padx=50, sticky="n")
        self.doctor_adress_male.grid(row=6, column=0, pady=(20, 0), padx=(70, 0), sticky="n")
        self.doctor_adress_female.grid(row=6, column=1, pady=(20, 0), padx=(0, 30), sticky="n")
        self.doctor_insurance_label.grid(row=7, column=0, columnspan=2, pady=(15, 0), sticky="n")
        self.doctor_insurance_checkbox_private.grid(row=8, column=0, columnspan=2, pady=(5, 0), padx=(50, 0), sticky="w")
        self.doctor_insurance_checkbox_by_law.grid(row=9, column=0, columnspan=2, pady=(8, 0), padx=(50, 0), sticky="w")
        self.doctor_insurance_checkbox_voluntarily.grid(row=10, column=0, columnspan=2, pady=(8, 0), padx=(50, 0), sticky="w")
        self.doctor_register_button.grid(row=11, column=0, columnspan=2, pady=(25, 20), padx=50, sticky="n")

    def try_patient_register(self, event=None) -> None:
        username = self.patient_username_entry.get()
        name = self.patient_name_entry.get()
        password = self.patient_password_entry.get()
        confirm_password = self.patient_confirm_password_entry.get()
        address = self.male.get()
        insurance = self.insurance_var.get()
        dental_problem = self.dental_problem_var.get()
        problem_teeth_count = self.teeth_count_spinbox.get()

        default_color = ("#979DA2", "#565B5E")

        entry_map = [
            [self.patient_username_entry, username == "", "no username given"],
            [self.patient_name_entry, name == "", "no name given"],
            [self.patient_password_entry, password == "", "no password given"],
            [self.patient_confirm_password_entry, confirm_password == "", "confirm your password"],
            [self.patient_confirm_password_entry, confirm_password != password, "your confirmation password does not match"],
            [self.insurance_combobox, insurance == "Krankenkassenart", "choose your type of insurance"],
            [self.dental_problem_combobox, dental_problem == "Dentale Problematik", "choose your dental problem"],
            [self.patient_username_entry, self.auth_service.username_exists(username), "username already exists"]]

        error_entrys = []
        for entry, is_problem, error_string in entry_map:
            if is_problem:
                error_entrys.append(entry)
                print(error_string)

        entrys = [self.patient_username_entry, self.patient_name_entry, self.patient_password_entry, self.patient_confirm_password_entry,
                  self.insurance_combobox, self.dental_problem_combobox]
        
        for entry in entrys:
            entry.configure(border_color=("red" if entry in error_entrys else default_color))

        if error_entrys:  # not empty
            return

        self.auth_service.add_patient({
            "username": username,
            # "name": name,
            # "adress": address,
            "password": password,
            "insurance": insurance,
            "dental_problem": dental_problem,
            "problem_teeth_count": problem_teeth_count
        })
        print("patient added")
        
        # delete entrys for privacy
        self.patient_username_entry.delete(0, "end")
        self.patient_name_entry.delete(0, "end")
        self.patient_password_entry.delete(0, "end")
        self.patient_confirm_password_entry.delete(0, "end")
        self.insurance_var.set("Krankenkassenart")
        self.dental_problem_combobox.set("Dentale Problematik")        
        
        # automatically log in
        self.nametowidget(".!ctkframe2.!canvas.!mainregisterframe").grid_forget()
        self.nametowidget(".").login_sidebar.grid_forget()
        self.nametowidget(".").main_grid()
        
    def try_doctor_register(self, event = None) -> None:
        username = self.doctor_username_entry.get()
        name = self.doctor_name_entry.get()
        address = self.male.get()
        password = self.doctor_password_entry.get()
        confirm_password = self.doctor_confirm_password_entry.get()
        insurance_private = self.insurance_private.get()
        insurance_by_law = self.insurance_by_law.get()
        insurance_voluntarily = self.insurance_voluntarily.get()
        
        default_color = ("#979DA2", "#565B5E")
        
        entry_map = [
            [self.doctor_username_entry, username == "", "no username given"],
            [self.doctor_name_entry, name == "", "no name given"],
            [self.doctor_password_entry, password == "", "no password given"],
            [self.doctor_confirm_password_entry, confirm_password == "", "confirm your password"],
            [self.doctor_confirm_password_entry, confirm_password != password, "your confirmation password does not match"],
            [self.doctor_insurance_checkbox_private, (insurance_voluntarily or insurance_by_law or insurance_private) == False , "choose at least one type of insurance"]]
        
        error_entrys = []
        for entry, is_problem, error_string in entry_map:
            if is_problem:
                error_entrys.append(entry)
                print(error_string)
                
        entrys = [self.doctor_username_entry, self.doctor_name_entry, self.doctor_password_entry, self.doctor_confirm_password_entry,
                  self.doctor_insurance_checkbox_private]
        
        for entry in entrys:
            if entry is self.doctor_insurance_checkbox_private:
                self.doctor_insurance_checkbox_by_law.configure(border_color=("red" if entry in error_entrys else default_color))
                self.doctor_insurance_checkbox_voluntarily.configure(border_color=("red" if entry in error_entrys else default_color))
            entry.configure(border_color=("red" if entry in error_entrys else default_color))

        if error_entrys:  # not empty
            return
        
        # self.auth_service.add_doctor({
        #     "username": username,
        #     # "name": name,
        #     # "address": address,
        #     "password": password,
        #     "insurance_private": insurance_private,
        #     "insurance_by_law": insurance_by_law,
        #     "insurance_voluntarily": insurance_voluntarily
        # })
        print("doctor added")
        
        # delete entrys for privacy
        self.doctor_username_entry.delete(0, "end")
        self.doctor_name_entry.delete(0, "end")
        self.doctor_password_entry.delete(0, "end")
        self.doctor_confirm_password_entry.delete(0, "end")
        self.insurance_private.set(False)
        self.insurance_by_law.set(False)
        self.insurance_voluntarily.set(False) 
        
        # automatically log in
        self.nametowidget(".!ctkframe2.!canvas.!mainregisterframe").grid_forget()
        self.nametowidget(".").login_sidebar.grid_forget()
        self.nametowidget(".").main_grid()
        