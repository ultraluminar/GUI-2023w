import tkinter as tk
import customtkinter as ctk
import logging

from source.classes.customWidgets.intSpinbox import IntSpinbox
from source.classes.timeSelector import TimeSelector
from source.auth_util import username_exists, add_patient, add_doctor, check_login, check_code

from CTkToolTip import CTkToolTip


class RegisterFormFrame(ctk.CTkTabview):
    """
    A custom frame class for a registration form with tabs for patients and doctors.

    This class extends the `ctk.CTkTabview` class and provides a user interface for registering as a patient or a doctor.
    It includes various input fields, buttons, and error handling.

    Methods:
        isVarAlpha(action_type: str, string: str) -> bool:
            Validates if a string contains only alphabetic characters.
        isVarAlNum(action_type: str, string: str) -> bool:
            Validates if a string contains only alphanumeric characters.
        set_patient_grid() -> None:
            Sets the grid layout for the patient registration section.
        set_doctor_grid() -> None:
            Sets the grid layout for the doctor registration section.
        try_patient_register(event=None) -> None:
            Attempts to register a patient based on the entered information.
        try_doctor_register(event=None) -> None:
            Attempts to register a doctor based on the entered information.
        time_selector() -> None:
            Opens the time slot selection window for the doctor.
        doctor_time_selector_saved(availability: list) -> None:
            Saves the selected availability for the doctor.
        reset() -> None:
            Resets the registration form to its initial state.
    """
    def __init__(self, master, bundle: dict):
        """
        Initializes the RegisterFormFrame.
        
        Args:
            master (tk.Widget): The parent widget for this frame.
            bundle (dict): A dictionary containing data bundle.
        """
        super().__init__(master=master)
        
        # tabs
        self.add("als Patient")
        self.add("als Zahnarzt")
        
        # variables
        self.input_width = 200
        self.data_bundle = bundle

        # font
        self.font15 = ctk.CTkFont(family="Segoe UI", size=15)
        
        # colors
        self.default_color = ("#979DA2", "#565B5E")
        self.button_default_color = ("#3B8ED0", "#1F6AA5")
        self.button_default_hover_color = ("#36719F", "#144870")

        # tk variables
        self.sex = tk.StringVar(value="Herr")
        # patient tab
        self.insurance_var = tk.StringVar(value="Krankenkassenart")
        self.dental_problem_var = tk.StringVar(value="Dentale Problematik")
        self.teeth_count_var = tk.IntVar()

        self.insurance_types = ["gesetzlich", "freiwillig gesetzlich", "privat"]
        self.dental_problem_types = ["Karies klein", "Karies groß", "Teilkrone", "Krone", "Wurzelbehandlung"]
        self.patient_error_string = tk.StringVar(value="")
        # doctor tab
        self.insurance_private = tk.BooleanVar(value=False)
        self.insurance_by_law = tk.BooleanVar(value=False)
        self.insurance_voluntarily = tk.BooleanVar(value=False)
        self.availability: list = []
        self.doctor_error_string = tk.StringVar(value="")

        # widgets
        # patient tab
        self.patient_heading = ctk.CTkLabel(self.tab("als Patient"), font=self.font15, text="Bitte hier registrieren")
        self.patient_username_entry = ctk.CTkEntry(self.tab("als Patient"), width=self.input_width, placeholder_text="Benutzername")
        self.patient_name_entry = ctk.CTkEntry(self.tab("als Patient"), width=self.input_width, placeholder_text="Nachname")
        self.patient_password_entry = ctk.CTkEntry(self.tab("als Patient"), width=self.input_width, placeholder_text="Passwort", show="•")
        self.patient_confirm_password_entry = ctk.CTkEntry(self.tab("als Patient"), width=self.input_width, placeholder_text="Passwort bestätigen", show="•")
        
        self.patient_adress_male = ctk.CTkRadioButton(self.tab("als Patient"), text="Herr", value="Herr", variable=self.sex)
        self.patient_adress_female = ctk.CTkRadioButton(self.tab("als Patient"), text="Frau", value="Frau", variable=self.sex)

        self.insurance_combobox = ctk.CTkComboBox(
            self.tab("als Patient"), width=self.input_width, values=self.insurance_types, variable=self.insurance_var, state="readonly")
        self.dental_problem_combobox = ctk.CTkComboBox(
            self.tab("als Patient"), width=self.input_width, values=self.dental_problem_types, variable=self.dental_problem_var, state="readonly")

        self.teeth_count_label = ctk.CTkLabel(self.tab("als Patient"), text="Anzahl zu behandelnder Zähne")
        self.teeth_count_spinbox = IntSpinbox(self.tab("als Patient"), width=self.input_width)
        self.patient_error_label = ctk.CTkLabel(self.tab("als Patient"), text_color="red", textvariable=self.patient_error_string)
        self.patient_register_button = ctk.CTkButton(self.tab("als Patient"), text="Registrieren", command=self.try_patient_register)
        
        # doctor tab
        self.doctor_heading = ctk.CTkLabel(self.tab("als Zahnarzt"), font=self.font15, text="Bitte hier registrieren")
        self.doctor_username_entry = ctk.CTkEntry(self.tab("als Zahnarzt"), width=self.input_width, placeholder_text="Benutzername")

        self.doctor_name_entry = ctk.CTkEntry(self.tab("als Zahnarzt"), width=self.input_width, placeholder_text="Nachname")
        self.doctor_name_entry.configure(validate="key", validatecommand=(self.doctor_username_entry.register(self.isVarAlpha), '%d', '%P'))

        self.doctor_password_entry = ctk.CTkEntry(self.tab("als Zahnarzt"), width=self.input_width, placeholder_text="Passwort", show="•")
        self.doctor_confirm_password_entry = ctk.CTkEntry(self.tab("als Zahnarzt"), width=self.input_width, placeholder_text="Passwort bestätigen", show="•")

        self.doctor_code = ctk.CTkEntry(self.tab("als Zahnarzt"), width=self.input_width, placeholder_text="Freischalt-Code")
        self.doctor_code.configure(validate="key", validatecommand=(self.doctor_code.register(self.isVarAlNum), '%d', '%P'))

        self.doctor_adress_male = ctk.CTkRadioButton(self.tab("als Zahnarzt"), text="Herr", value="Herr", variable=self.sex)
        self.doctor_adress_female = ctk.CTkRadioButton(self.tab("als Zahnarzt"), text="Frau", value="Frau", variable=self.sex)

        self.doctor_insurance_label = ctk.CTkLabel(self.tab("als Zahnarzt"), text="Welche Patienten behandeln Sie?")
        self.doctor_insurance_checkbox_private = ctk.CTkCheckBox(self.tab("als Zahnarzt"), text="Privatversicherte", variable=self.insurance_private)
        self.doctor_insurance_checkbox_by_law = ctk.CTkCheckBox(self.tab("als Zahnarzt"), text="Gesetzlichversicherte", variable=self.insurance_by_law)
        self.doctor_insurance_checkbox_voluntarily = ctk.CTkCheckBox(self.tab("als Zahnarzt"), text="freiwillig Gesetzlichversicherte", variable=self.insurance_voluntarily)
        
        self.time_selector_window = None
        self.doctor_time_selector_button = ctk.CTkButton(self.tab("als Zahnarzt"), width=self.input_width, text="Behandlungszeit auswählen", command=self.time_selector)
        self.doctor_error_label = ctk.CTkLabel(self.tab("als Zahnarzt"), text_color="red", textvariable=self.doctor_error_string)
        self.doctor_register_button = ctk.CTkButton(self.tab("als Zahnarzt"), text="Registrieren", command=self.try_doctor_register)
        
        # gridding
        self.set_patient_grid()
        self.set_doctor_grid()

        # tooltips
        CTkToolTip(self.patient_username_entry, message="Benutzername eingeben", alpha=0.8)
        CTkToolTip(self.patient_name_entry, message="Nachname eingeben", alpha=0.8)
        CTkToolTip(self.patient_password_entry, message="Passwort eingeben", alpha=0.8)
        CTkToolTip(self.patient_confirm_password_entry, message="Passwort bestätigen", alpha=0.8)
        CTkToolTip(self.insurance_combobox, message="Krankenkassenart auswählen", alpha=0.8)
        CTkToolTip(self.dental_problem_combobox, message="Dentale Problematik auswählen", alpha=0.8)
        CTkToolTip(self.teeth_count_spinbox, message="Anzahl der zu behandelnden Zähne auswählen", alpha=0.8)
        CTkToolTip(self.patient_register_button, message="Klicken um sich zu Registrieren (Enter)", alpha=0.8)

        CTkToolTip(self.doctor_username_entry, message="Benutzername eingeben", alpha=0.8)
        CTkToolTip(self.doctor_name_entry, message="Nachname eingeben", alpha=0.8)
        CTkToolTip(self.doctor_password_entry, message="Passwort eingeben", alpha=0.8)
        CTkToolTip(self.doctor_confirm_password_entry, message="Passwort bestätigen", alpha=0.8)
        CTkToolTip(self.doctor_code, message="Freischalt-Code eingeben", alpha=0.8)
        CTkToolTip(self.doctor_insurance_checkbox_private, message="Klicken wenn Sie Privatversicherte behandeln", alpha=0.8)
        CTkToolTip(self.doctor_insurance_checkbox_by_law, message="Klicken wenn Sie Gesetzlichversicherte behandeln", alpha=0.8)
        CTkToolTip(self.doctor_insurance_checkbox_voluntarily, message="Klicken wenn Sie freiwillig-Gesetzlichversicherte behandeln", alpha=0.8)
        CTkToolTip(self.doctor_time_selector_button, message="Klicken um Behandlungszeit auszuwählen", alpha=0.8)
        CTkToolTip(self.doctor_register_button, message="Klicken um sich zu Registrieren (Enter)", alpha=0.8)



    @staticmethod
    def isVarAlpha(action_type: str, string: str):
        """
        Check if the given string is alphabetic.

        Parameters:
        - action_type (str): The type of action being performed.
        - string (str): The string to be checked.

        Returns:
        - bool: True if the string is alphabetic, False otherwise.
        """
        if action_type != "1":
            return True

        return string.isalpha()

    @staticmethod
    def isVarAlNum(action_type: str, string: str):
        """
        Check if the given string is alphanumeric.

        Parameters:
        - action_type (str): The type of action being performed.
        - string (str): The string to be checked.

        Returns:
        - bool: True if the string is alphanumeric, False otherwise.
        """
        if action_type != "1":
            return True
        if len(string) > 8:
            return False
        return string.isalnum()
        

    def set_patient_grid(self):
        """
        Sets the grid layout for the patient form fields and widgets.
        """
        self.patient_heading.grid(row=1, column=0, columnspan=2, pady=(10, 0), padx=0, sticky="n")
        self.patient_username_entry.grid(row=2, column=0, columnspan=2, pady=(20, 0), padx=50, sticky="n")
        self.patient_name_entry.grid(row=3, column=0, columnspan=2, pady=(5, 0), padx=50, sticky="n")
        self.patient_password_entry.grid(row=4, column=0, columnspan=2, pady=(15, 0), padx=50, sticky="n")
        self.patient_confirm_password_entry.grid(row=5, column=0, columnspan=2, pady=(5, 0), padx=50, sticky="n")
        self.patient_adress_male.grid(row=6, column=0, pady=(20, 0), padx=(70, 0), sticky="n")
        self.patient_adress_female.grid(row=6, column=1, pady=(20, 0), padx=(0, 30), sticky="n")
        self.insurance_combobox.grid(row=7, column=0, columnspan=2, pady=(15, 0), padx=50, sticky="n")
        self.dental_problem_combobox.grid(row=8, column=0, columnspan=2, pady=(5, 0), padx=50, sticky="n")
        self.teeth_count_label.grid(row=9, column=0, columnspan=2, pady=(10, 0), padx=50, sticky="n")
        self.teeth_count_spinbox.grid(row=10, column=0, columnspan=2, pady=(2, 0), padx=50, sticky="n")
        self.patient_register_button.grid(row=12, column=0, columnspan=2, pady=(25, 20), padx=50, sticky="n")
        
    def set_doctor_grid(self):
        """
        Sets the grid layout for the doctor form fields and widgets.
        """
        self.doctor_heading.grid(row=1, column=0, columnspan=2, pady=(10, 0), padx=0, sticky="n")
        self.doctor_username_entry.grid(row=2, column=0, columnspan=2, pady=(20, 0), padx=50, sticky="n")
        self.doctor_name_entry.grid(row=3, column=0, columnspan=2, pady=(5, 0), padx=50, sticky="n")
        self.doctor_password_entry.grid(row=4, column=0, columnspan=2, pady=(15, 0), padx=50, sticky="n")
        self.doctor_confirm_password_entry.grid(row=5, column=0, columnspan=2, pady=(5, 0), padx=50, sticky="n")
        self.doctor_code.grid(row=6, column=0, columnspan=2, pady=(15, 0), padx=50, sticky="n")
        self.doctor_adress_male.grid(row=7, column=0, pady=(20, 0), padx=(70, 0), sticky="n")
        self.doctor_adress_female.grid(row=7, column=1, pady=(20, 0), padx=(0, 30), sticky="n")
        self.doctor_insurance_label.grid(row=8, column=0, columnspan=2, pady=(15, 0), sticky="n")
        self.doctor_insurance_checkbox_private.grid(row=9, column=0, columnspan=2, pady=(5, 0), padx=(50, 0), sticky="w")
        self.doctor_insurance_checkbox_by_law.grid(row=10, column=0, columnspan=2, pady=(8, 0), padx=(50, 0), sticky="w")
        self.doctor_insurance_checkbox_voluntarily.grid(row=11, column=0, columnspan=2, pady=(8, 0), padx=(50, 0), sticky="w")
        self.doctor_time_selector_button.grid(row=12, column=0, columnspan=2, pady=(15, 0), padx=50, sticky="n")
        self.doctor_register_button.grid(row=14, column=0, columnspan=2, pady=(25, 20), padx=50, sticky="n")

    def try_patient_register(self, *args) -> None:
        """
        Attempts to register a new patient with the provided information.

        This method retrieves the patient's details from the respective entry fields and checkboxes, validates 
        the input, and registers the patient if there are no errors. It provides visual feedback for errors by 
        changing the border color of the entry fields and checkboxes and displaying the error messages. If the 
        registration is successful, it logs the patient in and navigates to the home page.

        Args:
            event (Optional): The event that triggered the registration attempt. Defaults to None.
        """
        # get values
        username = self.patient_username_entry.get()
        name = self.patient_name_entry.get()
        password = self.patient_password_entry.get()
        confirm_password = self.patient_confirm_password_entry.get()
        address = self.sex.get()
        insurance = self.insurance_var.get()
        dental_problem = self.dental_problem_var.get()
        problem_teeth_count = self.teeth_count_spinbox.get()

        default_color = ("#979DA2", "#565B5E")

        
        entry_map = [
            [self.patient_username_entry, username == "", "Kein Benutzername angegeben"],
            [self.patient_name_entry, name == "", "Kein Nachname angegeben"],
            [self.patient_password_entry, password == "", "Kein Passwort angegeben"],
            [self.patient_confirm_password_entry, confirm_password == "", "Passwort nicht bestätigt"],
            [self.patient_confirm_password_entry, confirm_password != password, "Passwort stimmt nicht überein"],
            [self.insurance_combobox, insurance == "Krankenkassenart", "Wählen Sie Ihre Krankenkassenart"],
            [self.dental_problem_combobox, dental_problem == "Dentale Problematik", "Wählen Sie Ihre dentale Problematik"],
            [self.patient_username_entry, username_exists(username), "Benutzername bereits vergeben"]
        ]

        error_entrys = []
        error_messages = []
        for entry, is_problem, error_string in entry_map:
            if is_problem:
                error_entrys.append(entry)
                logging.warning(error_string)
                error_messages.append(error_string)
                

        entrys = [self.patient_username_entry, self.patient_name_entry, self.patient_password_entry, self.patient_confirm_password_entry,
                  self.insurance_combobox, self.dental_problem_combobox]
        
        # visual error feedback
        for entry in entrys:    # handling all entrys
            entry.configure(border_color=("red" if entry in error_entrys else default_color))
        if error_messages:  # not empty
            self.patient_error_string.set("\n".join(error_messages))
            self.patient_error_label.grid(row=11, column=0, columnspan=2, pady=(10, 0), padx=50, sticky="n")
        else:
            self.patient_error_label.grid_forget()

        if error_entrys:  # not empty
            return
        
        # create name with adress word
        name = f"{address} {name}"

        add_patient({
            "username": username,
            "name": name,
            "password": password,
            "insurance": insurance,
            "dental_problem": dental_problem,
            "problem_teeth_count": problem_teeth_count
        })
        logging.info(f"patient added to database ({username})")
        
        self.reset()     
        
        # automatically log in
        if check_login(username, password, self.data_bundle):
            # grid forget
            self.nametowidget(".!ctkframe2.!canvas.!mainregisterframe").grid_forget()
            self.nametowidget(".").login_sidebar.grid_forget()
            # grid
            self.nametowidget(".").main_sidebar_grid()
            self.nametowidget(".").home_grid()
        else: 
            raise PermissionError
        
    def try_doctor_register(self, *args) -> None:
        """
        Attempts to register a new doctor.

        This method retrieves the doctor's details from the respective entry fields and checkboxes, checks for 
        any errors such as empty fields or incorrect OTP, and registers the doctor if there are no errors. It 
        also provides visual feedback for errors by changing the border color of the entry fields and checkboxes 
        and displaying the error messages. If the registration is successful, it logs the doctor in and navigates 
        to the doctor's page.
        """
        username = self.doctor_username_entry.get()
        name = self.doctor_name_entry.get()
        address = self.sex.get()
        password = self.doctor_password_entry.get()
        confirm_password = self.doctor_confirm_password_entry.get()
        code = self.doctor_code.get()
        insurance_private = self.insurance_private.get()
        insurance_by_law = self.insurance_by_law.get()
        insurance_voluntarily = self.insurance_voluntarily.get()
        insurances = [insurance_voluntarily, insurance_by_law, insurance_private]
        otp_verified = code != "" and check_code(code, self.data_bundle)
        
        entry_map = [
            [self.doctor_username_entry,             username == "",                "Kein Benutzername angegeben"],
            [self.doctor_name_entry,                 name == "",                    "Kein Nachname angegeben"],
            [self.doctor_password_entry,             password == "",                "Kein Passwort angegeben"],
            [self.doctor_confirm_password_entry,     confirm_password == "",        "Passwort nicht bestätigt"],
            [self.doctor_confirm_password_entry,     confirm_password != password,  "Passwort stimmt nicht überein"],
            [self.doctor_insurance_checkbox_private, not any(insurances),           "Wählen mindestens eine Krankenkassenart"],
            [self.doctor_time_selector_button,       self.availability == [],       "Wählen Sie einen Behandlungszeitraum"],
            [self.doctor_username_entry,             username_exists(username),     "Benutzername bereits vergeben"],
            [self.doctor_code, code == "", "Kein Freischalt-Code angegeben"],
            [self.doctor_code, not otp_verified, "Freischalt-Code ungültig"]]
        
        error_entrys = []
        error_messages = []
        for entry, is_problem, error_string in entry_map:
            if is_problem:
                error_entrys.append(entry)
                logging.warning(error_string)
                error_messages.append(error_string)
                
        entrys = [self.doctor_username_entry, self.doctor_name_entry, self.doctor_password_entry, self.doctor_confirm_password_entry,
                  self.doctor_insurance_checkbox_private, self.doctor_code]
        
        # visual error feedback
        for entry in entrys:
            if entry is self.doctor_insurance_checkbox_private: # handling all checkboxes if none are ticked
                self.doctor_insurance_checkbox_by_law.configure(border_color=("red" if entry in error_entrys else self.default_color))
                self.doctor_insurance_checkbox_voluntarily.configure(border_color=("red" if entry in error_entrys else self.default_color))
            entry.configure(border_color=("red" if entry in error_entrys else self.default_color))
        self.doctor_time_selector_button.configure(fg_color="red" if self.doctor_time_selector_button in error_entrys else self.button_default_color)
        if error_messages:  # not empty
            self.doctor_error_string.set("\n".join(error_messages))
            self.doctor_error_label.grid(row=13, column=0, columnspan=2, pady=(10, 0), padx=50, sticky="n")
        else:
            self.doctor_error_label.grid_forget()

        if error_entrys:  # not empty
            return

        # create name with adress word
        name = f"{address} Dr. {name}"
        
        add_doctor({
            "username": username,
            "name": name,
            "password": password,
            "insurance_private": insurance_private,
            "insurance_by_law": insurance_by_law,
            "insurance_voluntarily": insurance_voluntarily,
            "availability": self.availability
        })
        logging.info(f"doctor added to database ({username})")
        
        self.reset()
        
        # automatically log in
        if check_login(username, password, self.data_bundle):
            # grid forget
            self.nametowidget(".!ctkframe2.!canvas.!mainregisterframe").grid_forget()
            self.nametowidget(".").login_sidebar.grid_forget()
            # grid
            self.nametowidget(".").doctor_grid()
        else:
            raise PermissionError
        
        #destroy time selector window
        if self.time_selector_window is not None:
            self.time_selector_window.destroy()
        
        
    def time_selector(self):
        """
        Opens the time selector window.

        If the time selector window is not created or destroyed, it creates a new window.
        If the time selector window is minimized or withdrawn, it brings back the window.
        Otherwise, it focuses on the existing time selector window.
        """
        if self.time_selector_window is None or not self.time_selector_window.winfo_exists():
            self.time_selector_window = TimeSelector(self)     # create window if it's None or destroyed
            self.after(100, lambda: self.time_selector_window.focus())
        elif self.time_selector_window.state() in ("iconic", "withdrawn"):
            self.time_selector_window.deiconify()    # bring back window if it's minimized
        else:
            self.time_selector_window.focus()
        
    def doctor_time_selector_saved(self, availability: list):
        """
        Saves the selected availability for the doctor and updates the button text and color.

        Args:
            availability (list): The list of available time slots.
        """
        self.availability = availability
        
        # visual feedback
        self.doctor_time_selector_button.configure(fg_color=("#26a31d", "#369130"), hover_color=("#1d8017", "#2c7527"), text="Behandlungszeit ändern")
    
    def reset(self):
        """
        Resets the registration form to its initial state.

        This method clears all the patient and doctor entry fields and checkboxes, resets the comboboxes and 
        spinbox to their default values, hides the error labels, and reverts the border color of the entry fields 
        and checkboxes to the default color. It also clears the doctor's availability and destroys the time 
        selector window if it exists.
        """
        # delete patient entrys for privacy
        self.patient_username_entry.delete(0, "end")
        self.patient_name_entry.delete(0, "end")
        self.patient_password_entry.delete(0, "end")
        self.patient_confirm_password_entry.delete(0, "end")
        self.insurance_var.set("Krankenkassenart")
        self.dental_problem_combobox.set("Dentale Problematik")
        self.teeth_count_spinbox.set(1)
        # delete patient error label
        self.patient_error_label.grid_forget()
        # revert patient error colorings
        for entry in [self.patient_username_entry, self.patient_name_entry, self.patient_password_entry, self.patient_confirm_password_entry,
                      self.insurance_combobox, self.dental_problem_combobox]:
            entry.configure(border_color=self.default_color)
        
        # delete doctor entrys for privacy
        for entry in [self.doctor_username_entry, self.doctor_name_entry,
                      self.doctor_password_entry, self.doctor_confirm_password_entry,
                      self.doctor_code]:
            entry.delete(0, "end")
        for insurance in [self.insurance_private, self.insurance_by_law, self.insurance_voluntarily]:
            insurance.set(False)
            
        self.availability = []
        # delete doctor error label
        self.doctor_error_label.grid_forget()
        # revert doctor error colorings
        for entry in [self.doctor_username_entry, self.doctor_name_entry, self.doctor_password_entry, self.doctor_confirm_password_entry,
                      self.doctor_code]:
            entry.configure(border_color=self.default_color)
        self.doctor_time_selector_button.configure(fg_color=self.button_default_color, hover_color=self.button_default_hover_color, text="Behandlungszeit auswählen")

        # destroy time selector window
        if self.time_selector_window is not None:
            self.time_selector_window.destroy()
            self.time_selector_window = None
        