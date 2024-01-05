import customtkinter as ctk
import tkinter as tk
from datetime import datetime

from pandas import read_csv

class PatientOverview(ctk.CTkFrame):
    """
    A custom widget for displaying patient appointment overview.

    Methods:
        __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: int | str | None = None):
            Initializes the PatientOverview widget.
        
        reset(self):
            Resets the widget by updating the appointment data and refreshing the table.
        
        table_ungrid(self):
            Removes all labels from the table.
        
        table_grid(self):
            Displays the labels in the table.
        
        get_doctor_name(self, username: str) -> str:
            Retrieves the name of the doctor based on the username.
    """
    
    def __init__(self, master: any, bundle: dict, width: int = 200, height: int = 200, corner_radius: int | str | None = None):
        """
        Initializes the PatientOverview widget.

        Args:
            master (any): The master widget.
            bundle (dict): A dictionary containing the user data.
            width (int): The width of the widget. Default is 200.
            height (int): The height of the widget. Default is 200.
            corner_radius (int | str | None): The corner radius of the widget. Default is None.
        """
        super().__init__(master, width, height, corner_radius)

        self.df_appointments = None
        self.data_bundle = bundle
        
        self.headings: list[str] = ["Datum", "Arzt", "Von", "Bis", "Zahnproblem", "Anzahl Zähne", "Art der Füllung"]
        self.header_labels: list[ctk.CTkLabel] = [ctk.CTkLabel(self, width=110, height=30, fg_color=("gray70", "gray30"), corner_radius=5, text=heading, font=ctk.CTkFont(weight="bold")) for heading in self.headings]
        self.empty_label = ctk.CTkLabel(self, text="Keine Termine vorhanden. Buchen sie ihren nächsten Termin über den Button unten\noder über die Navigationsleiste unter Termin buchen")
        
        # initializing lists to store attribute labels and storeing them in master list
        self.date_labels: list[ctk.CTkLabel] = []
        self.doctor_labels: list[ctk.CTkLabel] = []
        self.time_start_labels: list[ctk.CTkLabel] = []
        self.time_end_labels: list[ctk.CTkLabel] = []
        self.dental_problem_labels: list[ctk.CTkLabel] = []
        self.teeth_count_labels: list[ctk.CTkLabel] = []
        self.fill_type_labels: list[ctk.CTkLabel] = []
    
    def reset(self):
        """
        Resets the widget by updating the appointment data and refreshing the table.
        """
        self.table_ungrid()
        self.df_appointments = read_csv("data/appointments.csv")
        self.df_appointments = self.df_appointments.loc[self.df_appointments["Patient"] == self.data_bundle["username"]]
        self.df_appointments = self.df_appointments.loc[self.df_appointments["dt_stop"] > datetime.now().strftime("%d-%m-%Y %H:%M")]   # filter out appointments that are already over
        self.df_appointments = self.df_appointments.sort_values("dt_start")
        
        self.date_labels = [ctk.CTkLabel(self, text=date.split(" ")[0]) for date in self.df_appointments["dt_start"]]
        self.doctor_labels = [ctk.CTkLabel(self, text=self.get_doctor_name(doctor)) for doctor in self.df_appointments["Doctor"]]
        self.time_start_labels = [ctk.CTkLabel(self, text=time.split(" ")[1]) for time in self.df_appointments["dt_start"]]
        self.time_end_labels = [ctk.CTkLabel(self, text=time.split(" ")[1]) for time in self.df_appointments["dt_stop"]]
        self.dental_problem_labels = [ctk.CTkLabel(self, text=dental_problem) for dental_problem in self.df_appointments["dental_problem"]]
        self.teeth_count_labels = [ctk.CTkLabel(self, text=tooth_count) for tooth_count in self.df_appointments["tooth_count"]]
        self.fill_type_labels = [ctk.CTkLabel(self, text=fill_type) for fill_type in self.df_appointments["fill_type"]]
        
        self.table_grid()

    def table_ungrid(self):
        """
        Removes all labels from the table.
        """
        self.empty_label.grid_forget()
        labels = [self.date_labels, self.doctor_labels, self.time_start_labels, self.time_end_labels, self.dental_problem_labels, self.teeth_count_labels, self.fill_type_labels]
        for labels in labels:
            for label in labels:
                label.grid_forget()
            
    def table_grid(self):
        """
        Displays the labels in the table.
        """
        for index, label in enumerate(self.header_labels):
            label.grid(column=index, row=0, sticky="nsew", padx=(10 if index == 0 else 5, 10 if index == 6 else 0), pady=(10, 15))
        if self.df_appointments.empty:
            self.empty_label.grid(column=0, row=1, columnspan=7, sticky="nsew", padx=10, pady=(0, 10))
        labels = [self.date_labels, self.doctor_labels, self.time_start_labels, self.time_end_labels, self.dental_problem_labels, self.teeth_count_labels, self.fill_type_labels]
        for index, labels in enumerate(labels):
            for label in labels:
                label.grid(column=index, row=labels.index(label) + 1, sticky="nsew", padx=(10 if index == 0 else 5, 10 if index == 6 else 0), pady=(0, 10))
        
    def get_doctor_name(self, username: str) -> str:
        """
        Retrieves the name of the doctor based on the username.

        Args:
            username (str): The username of the doctor.

        Returns:
            str: The name of the doctor.
        """
        df_doctors = read_csv("data/doctors.csv")
        return df_doctors.loc[df_doctors["Username"] == username, "Name"].iloc[0]