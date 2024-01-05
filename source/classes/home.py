import customtkinter as ctk

from pandas import read_csv
from datetime import datetime

from source.classes.customWidgets.patientAppointmentOverview import PatientOverview
from source.classes.customWidgets.infoBanner import InfoBanner

from source.auth_util import getfromCSV, paths

class HomeFrame(ctk.CTkScrollableFrame):
    """
    A custom frame class representing the home screen of the GUI application.

    Methods:
        __init__(self, master: ctk.CTk, bundle: dict):
            Initializes the HomeFrame.
        set_main_grid(self):
            Sets the grid layout for the main widgets.
        set_profile_grid(self):
            Sets the grid layout for the profile sub frame widgets.
        set_appointments_grid(self):
            Sets the grid layout for the appointments sub frame widgets.
        reset(self):
            Resets the HomeFrame by updating the displayed information.
        get_patient_name(self):
            Retrieves the name of the patient from the data source.
        get_insurace_type(self):
            Retrieves the insurance type of the patient from the data source.
        get_dental_problem(self):
            Retrieves the dental problem of the patient from the data source.
        get_tooth_number(self):
            Retrieves the total number of teeth to be treated for the patient from the data source.
        get_tooth_number_with_appointment(self):
            Retrieves the number of teeth to be treated in the next 3 months for the patient from the data source.
        book_appointment(self):
            Books an appointment for the patient.
        displayAppointmentFeedback(self):
            Displays the appointment feedback.
    """
    def __init__(self, master: ctk.CTk, bundle: dict):
        """
        Initializes the HomeFrame.

        Args:
            master (ctk.CTk): The master widget.
            bundle (dict): A dictionary containing data bundle.
        """
        super().__init__(master=master, corner_radius=0, fg_color="transparent")

        self.data_bundle = bundle
        
        self.grid_columnconfigure(0, weight=1)
        
        # fonts
        font30 = ctk.CTkFont(family="Segoe UI", size=30, weight="bold")
        font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        fat = ctk.CTkFont(family="Segoe UI", weight="bold")
        
        # main widgets
        self.main_heading_label = ctk.CTkLabel(self, text=f"Willkommen, ERROR!", font=font30)
        self.sub_heading_label = ctk.CTkLabel(self, text="Was möchten sie tun?")
        self.info_banner = InfoBanner(self, self.data_bundle)
        
        # profil sub Frame
        self.profil_frame = ctk.CTkFrame(self)
        self.profil_frame.grid_columnconfigure((0, 3), weight=1)
        self.profil_heading_label = ctk.CTkLabel(self.profil_frame, text="Mein Profil", font=font24)
        self.profil_sub_heading_label = ctk.CTkLabel(self.profil_frame, text="Hier können sie ihre Daten einsehen.")
        self.insurance_type_label = ctk.CTkLabel(self.profil_frame, text="Ihre Versicherungsart:", anchor="w", width=280)
        self.insurance_value_label = ctk.CTkLabel(self.profil_frame, width=110, anchor="w", font=fat)
        self.dental_problem_type_label = ctk.CTkLabel(self.profil_frame, text="Ihr Zahnproblem:", anchor="w", width=280)
        self.dental_problem_value_label = ctk.CTkLabel(self.profil_frame, width=110, anchor="w", font=fat)
        self.tooth_number_label = ctk.CTkLabel(self.profil_frame, text="Ihre Anzahl noch zu behandelnder Zähne:", anchor="w", width=280)
        self.tooth_number_value_label = ctk.CTkLabel(self.profil_frame, width=110, anchor="w", font=fat)
        self.tooth_number_with_appointment_label = ctk.CTkLabel(self.profil_frame, text="Davon in den nächsten 3 Monaten behandelt:", anchor="w", width=280)
        self.tooth_number_with_appointment_value_label = ctk.CTkLabel(self.profil_frame, width=110, anchor="w", font=fat)
        
        # appointments sub Frame
        self.appointments_frame = ctk.CTkFrame(self)
        self.appointments_frame.grid_columnconfigure((0, 2), weight=1)
        self.appointments_heading_label = ctk.CTkLabel(self.appointments_frame, text="Meine Termine", font=font24)
        self.appointments_sub_heading_label = ctk.CTkLabel(self.appointments_frame, text="Hier können sie ihre Termine einsehen.")
        self.appointments_sub_frame = PatientOverview(self.appointments_frame, self.data_bundle)
        self.book_appointment_button = ctk.CTkButton(self.appointments_frame, text="Termin buchen", command=self.book_appointment)
        
        self.set_profile_grid()
        self.set_appointments_grid()
        self.set_main_grid()
        
    def set_main_grid(self):
        """
        Sets the grid layout for the main widgets.
        """
        self.main_heading_label.grid(row=0, column=0, columnspan=2, pady=(10, 0), sticky="nsew")
        self.sub_heading_label.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="nsew")
        self.profil_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.appointments_frame.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
    def set_profile_grid(self):
        """
        Sets the grid layout for the profile sub frame widgets.
        """
        self.profil_heading_label.grid(row=0, column=1, columnspan=2, pady=(10, 0))
        self.profil_sub_heading_label.grid(row=1, column=1, columnspan=2, pady=(0, 10))
        self.insurance_type_label.grid(row=2, column=1, pady=(10, 0))
        self.insurance_value_label.grid(row=2, column=2, pady=(10, 0))
        self.dental_problem_type_label.grid(row=3, column=1, pady=(10, 0))
        self.dental_problem_value_label.grid(row=3, column=2, pady=(10, 0))
        self.tooth_number_label.grid(row=4, column=1, pady=(10, 0))
        self.tooth_number_value_label.grid(row=4, column=2, pady=(10, 0))
        self.tooth_number_with_appointment_label.grid(row=5, column=1, pady=(10, 15))
        self.tooth_number_with_appointment_value_label.grid(row=5, column=2, pady=(10, 15))
    
    def set_appointments_grid(self):
        """
        Sets the grid layout for the appointments sub frame widgets.
        """
        self.appointments_heading_label.grid(row=0, column=1, pady=(10, 0))
        self.appointments_sub_heading_label.grid(row=1, column=1, pady=(0, 10))
        self.appointments_sub_frame.grid(row=2, column=1, pady=(0, 10))
        self.book_appointment_button.grid(column=0, columnspan=3, row=3, pady=20, sticky="e", padx=(0, 20))
        
    def reset(self):
        """
        Resets the HomeFrame by updating the displayed information.
        """
        kwargs = {"path": paths["patients"]["csv"], "filter_tuple": ("Username", self.data_bundle["username"])}
        username = getfromCSV(**kwargs, field="Name")
        insurace_type = getfromCSV(**kwargs, field="Krankenkassenart")
        dental_problem = getfromCSV(**kwargs, field="Dentale Problematik")
        tooth_number = getfromCSV(**kwargs, field="Anzahl zu behandelnder Zähne")
        tooth_number += self.get_tooth_number_with_appointment()

        self.main_heading_label.configure(text=f"Willkommen, {username}!")
        self.insurance_value_label.configure(text=insurace_type)
        self.dental_problem_value_label.configure(text=dental_problem)
        self.tooth_number_value_label.configure(text=tooth_number)
        self.tooth_number_with_appointment_value_label.configure(text=self.get_tooth_number_with_appointment())
        self.appointments_sub_frame.reset()


    def get_tooth_number_with_appointment(self):
        """
        Retrieves the number of teeth to be treated in the next 3 months for the patient from the data source.

        Returns:
            int: The number of teeth to be treated in the next 3 months.
        """
        df = read_csv("data/appointments.csv")
        # filter out appointments that are already over
        df = df.loc[df["dt_stop"] > datetime.now().strftime("%d-%m-%Y %H:%M")]
        # filter out appointments that are not for the patient
        df = df.loc[df["Patient"] == self.data_bundle["username"]]
        return df["tooth_count"].sum()
        
    def book_appointment(self):
        """
        Books an appointment for the patient.
        """
        self.nametowidget(".!mainsidebar").book_event()

    def displayAppointmentFeedback(self):
        """
        Displays the appointment feedback.
        """
        self.info_banner.grid(row=2, column=0, columnspan=3, sticky="ns", pady=(0, 20), padx=20)
        self.info_banner.show()
        self.info_banner.grid_forget()
    
        