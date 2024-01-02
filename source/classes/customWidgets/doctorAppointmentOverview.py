import customtkinter as ctk
import tkinter as tk
from datetime import datetime

from pandas import read_csv

class DoctorOverview(ctk.CTkFrame):
    def __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: int | str | None = None):
        super().__init__(master, width, height, corner_radius)
        
        self.auth_service = self.nametowidget(".").auth_service
        self.username = None
        df_appointments = None
        
        self.headings: list[str] = ["Datum", "Patient", "Von", "Ende", "Zahnproblem", "Anzahl Zähne", "Art der Füllung"]
        self.header_labels: list[ctk.CTkLabel] = [ctk.CTkLabel(self, width=110, height=30, fg_color=("gray70", "gray30"), corner_radius=5, text=heading, font=ctk.CTkFont(weight="bold")) for heading in self.headings]
        self.empty_label = ctk.CTkLabel(self, text="Keine Termine vorhanden. Bei ihnen wurden noch keine Termine gebucht.")
        
        # initializing lists to store attribute labels and storeing them in master list
        self.date_labels: list[ctk.CTkLabel] = []
        self.patient_labels: list[ctk.CTkLabel] = []
        self.time_start_labels: list[ctk.CTkLabel] = []
        self.time_end_labels: list[ctk.CTkLabel] = []
        self.dental_problem_labels: list[ctk.CTkLabel] = []
        self.teeth_count_labels: list[ctk.CTkLabel] = []
        self.fill_type_labels: list[ctk.CTkLabel] = []
        self.labels = [self.date_labels, self.patient_labels, self.time_start_labels, self.time_end_labels, self.dental_problem_labels, self.teeth_count_labels, self.fill_type_labels]
    
    def reset(self):
        self.table_ungrid()
        self.username = self.auth_service.username
        self.df_appointments = read_csv("data/appointments.csv")
        self.df_appointments = self.df_appointments.loc[self.df_appointments["Doctor"] == self.username]
        self.df_appointments = self.df_appointments.sort_values("dt_start")
        
        
        self.date_labels = [ctk.CTkLabel(self, text=datetime.fromisoformat(date).strftime("%d.%m.%Y")) for date in self.df_appointments["dt_start"]]
        self.patient_labels = [ctk.CTkLabel(self, text=self.get_patient_name(patient)) for patient in self.df_appointments["Patient"]]
        self.time_start_labels = [ctk.CTkLabel(self, text=datetime.fromisoformat(time).strftime("%H:%M Uhr")) for time in self.df_appointments["dt_start"]]
        self.time_end_labels = [ctk.CTkLabel(self, text=datetime.fromisoformat(time).strftime("%H:%M Uhr")) for time in self.df_appointments["dt_stop"]]
        self.dental_problem_labels = [ctk.CTkLabel(self, text=dental_problem) for dental_problem in self.df_appointments["dental_problem"]]
        self.teeth_count_labels = [ctk.CTkLabel(self, text=tooth_count) for tooth_count in self.df_appointments["tooth_count"]]
        self.fill_type_labels = [ctk.CTkLabel(self, text=fill_type) for fill_type in self.df_appointments["fill_type"]]
        
        self.table_grid()
        
    def table_ungrid(self):
        self.empty_label.grid_forget()
        for labels in self.labels:
            for label in labels:
                label.grid_forget()
            
    def table_grid(self):
        for index, label in enumerate(self.header_labels):
            label.grid(column=index, row=0, sticky="nsew", padx=(10 if index == 0 else 5, 10 if index == 6 else 0), pady=(10, 15))
        if (self.df_appointments.empty):
            self.empty_label.grid(column=0, row=1, columnspan=7, sticky="nsew", padx=10, pady=(0, 10))
        for index, labels in enumerate(self.labels):
            for label in labels:
                label.grid(column=index, row=labels.index(label) + 1, sticky="nsew", padx=(10 if index == 0 else 5, 10 if index == 6 else 0), pady=(0, 10))
        
    def get_patient_name(self, username: str) -> str:
        df_patients = read_csv("data/patients.csv")
        return df_patients.loc[df_patients["Username"] == self.username, "Name"].iloc[0]