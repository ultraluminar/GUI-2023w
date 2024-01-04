import customtkinter as ctk

from pandas import read_csv
from datetime import datetime

from source.classes.customWidgets.patientAppointmentOverview import PatientOverview
from source.classes.customWidgets.infoBanner import InfoBanner

class HomeFrame(ctk.CTkScrollableFrame):
    def __init__(self, master: ctk.CTk, bundle: dict):
        super().__init__(master=master, corner_radius=0)
        
        self.auth_service = self.nametowidget(".").auth_service
        self.username = None
        self.data_bundle = bundle
        
        self.grid_columnconfigure(0, weight=1)
        
        # fonts
        font30 = ctk.CTkFont(family="Segoe UI", size=30, weight="bold")
        font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        fat = ctk.CTkFont(family="Segoe UI", weight="bold")
        
        # main widgets
        self.main_heading_label = ctk.CTkLabel(self, text=f"Willkommen, {self.username}!", font=font30)
        self.sub_heading_label = ctk.CTkLabel(self, text="Was möchten sie tun?")
        
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
        self.appointments_sub_frame = PatientOverview(self.appointments_frame)
        self.book_appointment_button = ctk.CTkButton(self.appointments_frame, text="Termin buchen", command=self.book_appointment)
        
        self.set_profile_grid()
        self.set_appointments_grid()
        self.set_main_grid()
        
    def set_main_grid(self):
        self.main_heading_label.grid(row=0, column=0, columnspan=2, pady=(10, 0), sticky="nsew")
        self.sub_heading_label.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="nsew")
        self.profil_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.appointments_frame.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
    def set_profile_grid(self):
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
        self.appointments_heading_label.grid(row=0, column=1, pady=(10, 0))
        self.appointments_sub_heading_label.grid(row=1, column=1, pady=(0, 10))
        self.appointments_sub_frame.grid(row=2, column=1, pady=(0, 10))
        self.book_appointment_button.grid(column=0, columnspan=3, row=3, pady=20, sticky="e", padx=(0, 20))
        
    def reset(self):
        self.username = self.auth_service.username
        self.main_heading_label.configure(text=f"Willkommen, {self.get_patient_name()}!")
        self.insurance_value_label.configure(text=self.get_insurace_type())
        self.dental_problem_value_label.configure(text=self.get_dental_problem())
        self.tooth_number_value_label.configure(text=self.get_tooth_number())
        self.tooth_number_with_appointment_value_label.configure(text=self.get_tooth_number_with_appointment())
        self.appointments_sub_frame.reset()
        
    def get_patient_name(self):
        df = read_csv("data/patients.csv")
        return df.loc[df["Username"] == self.username, "Name"].iloc[0]
    
    def get_insurace_type(self):
        df = read_csv("data/patients.csv")
        return df.loc[df["Username"] == self.username, "Krankenkassenart"].iloc[0]
    
    def get_dental_problem(self):
        df = read_csv("data/patients.csv")
        return df.loc[df["Username"] == self.username, "Dentale Problematik"].iloc[0]
    
    def get_tooth_number(self):
        df = read_csv("data/patients.csv")
        return df.loc[df["Username"] == self.username, "Anzahl zu behandelnder Zähne"].iloc[0] + self.get_tooth_number_with_appointment()
    
    def get_tooth_number_with_appointment(self):
        df = read_csv("data/appointments.csv")
        # filter out appointments that are already over
        df = df.loc[df["dt_stop"] > datetime.now().strftime("%d-%m-%Y %H:%M")]
        # filter out appointments that are not for the patient
        df = df.loc[df["Patient"] == self.username]
        return df["tooth_count"].sum()
        
    def book_appointment(self):
        self.nametowidget(".!mainsidebar").book_event()

    def displayAppointmentFeedback(self):
        info_banner = InfoBanner(self, text=f"Termin gebucht: {self.data_bundle['appointment_row'][2]}")
        info_banner.grid(row=2, column=0, columnspan=3, sticky="ns", pady=(0, 20), padx=20)
        info_banner.show()
        print("showed info banner")
    
        