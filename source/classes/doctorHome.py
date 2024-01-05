import customtkinter as ctk
import json

import pandas as pd
from pandas import read_csv
from dateutil.rrule import rrulestr, rruleset
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta, MO, SA

from source.classes.customWidgets.doctorAppointmentOverview import DoctorOverview

class DoctorHome(ctk.CTkScrollableFrame):
    """
    A class representing the doctor's home page.

    Attributes:
        auth_service (AuthService): The authentication service.
        username (str): The username of the doctor.

    Methods:
        __init__(self, master: ctk.CTk): Initializes the DoctorHome instance.
        set_main_grid(self): Sets the grid layout for the main widgets.
        set_profile_grid(self): Sets the grid layout for the profile sub-frame.
        set_appointments_grid(self): Sets the grid layout for the appointments sub-frame.
        reset(self): Resets the doctor's home page.
        get_doctor_name(self) -> str: Retrieves the name of the doctor from a CSV file.
        get_treated_insurance_types(self) -> str: Retrieves the types of insurance the doctor treats.
        get_weekly_hours(self) -> int: Calculates the number of weekly working hours for the doctor.
        get_appointments_week(self) -> int: Calculates the number of appointments for the current week.
        get_appointments_day(self) -> int: Calculates the number of appointments for the current day.
        count_appointments(self, date: date) -> int: Counts the number of appointments for a specific date.
        get_next_week_days(self) -> List[date]: Retrieves the dates of the next week.
        book_appointment(self): Books an appointment for the doctor.
    """
    def __init__(self, master: ctk.CTk, bundle: dict):
        """
        Initializes the DoctorHome instance.

        Args:
            master (ctk.CTk): The master widget.
        """
        super().__init__(master=master, corner_radius=0, fg_color="transparent")

        
        self.grid_columnconfigure(0, weight=1)
        self.data_bundle = bundle

        # fonts
        font30 = ctk.CTkFont(family="Segoe UI", size=30, weight="bold")
        font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        fat = ctk.CTkFont(family="Segoe UI", weight="bold")
        
        # main widgets
        self.main_heading_label = ctk.CTkLabel(self, text=f"Willkommen, ERROR!", font=font30)
        self.sub_heading_label = ctk.CTkLabel(self, text="Was möchten sie tun?")
        
        # profil sub Frame
        self.profil_frame = ctk.CTkFrame(self)
        self.profil_frame.grid_columnconfigure((0, 3), weight=1)
        self.profil_heading_label = ctk.CTkLabel(self.profil_frame, text="Mein Profil", font=font24)
        self.profil_sub_heading_label = ctk.CTkLabel(self.profil_frame, text="Hier können sie ihre Daten einsehen.")
        self.insurance_type_label = ctk.CTkLabel(self.profil_frame, text="Sie behandeln:", anchor="w", width=280)
        self.insurance_value_label = ctk.CTkLabel(self.profil_frame, width=230, anchor="w", font=fat)
        self.weekly_hours_label = ctk.CTkLabel(self.profil_frame, text="Arbeitszeit:", anchor="w", width=280)
        self.weekly_hours_value_label = ctk.CTkLabel(self.profil_frame, width=230, anchor="w", font=fat)
        self.number_appointments_week_label = ctk.CTkLabel(self.profil_frame, text="Anzahl anstehender Termine diese Woche:", anchor="w", width=280)
        self.number_appointments_week_value_label = ctk.CTkLabel(self.profil_frame, width=230, anchor="w", font=fat)
        self.number_appointments_today_label = ctk.CTkLabel(self.profil_frame, text="Davon Termine noch heute:", anchor="w", width=280)
        self.number_appointments_today_value_label = ctk.CTkLabel(self.profil_frame, width=230, anchor="w", font=fat)
        
        # appointments sub Frame
        self.appointments_frame = ctk.CTkFrame(self)
        self.appointments_frame.grid_columnconfigure((0, 2), weight=1)
        self.appointments_heading_label = ctk.CTkLabel(self.appointments_frame, text="Meine Termine", font=font24)
        self.appointments_sub_heading_label = ctk.CTkLabel(self.appointments_frame, text="Hier können sie ihre Termine einsehen.")
        self.appointments_sub_frame = DoctorOverview(self.appointments_frame, self.data_bundle)
        
        self.set_profile_grid()
        self.set_appointments_grid()
        self.set_main_grid()
        
    def set_main_grid(self):
        """
        Sets the grid layout for the main widgets.
        """
        self.main_heading_label.grid(row=0, column=0, columnspan=2, pady=(10, 0), sticky="nsew")
        self.sub_heading_label.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="nsew")
        self.profil_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.appointments_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
    def set_profile_grid(self):
        """
        Sets the grid layout for the profile sub-frame.
        """
        self.profil_heading_label.grid(row=0, column=1, columnspan=2, pady=(10, 0))
        self.profil_sub_heading_label.grid(row=1, column=1, columnspan=2, pady=(0, 10))
        self.insurance_type_label.grid(row=2, column=1, pady=(10, 0))
        self.insurance_value_label.grid(row=2, column=2, pady=(10, 0))
        self.weekly_hours_label.grid(row=3, column=1, pady=(10, 0))
        self.weekly_hours_value_label.grid(row=3, column=2, pady=(10, 0))
        self.number_appointments_week_label.grid(row=4, column=1, pady=(10, 0))
        self.number_appointments_week_value_label.grid(row=4, column=2, pady=(10, 0))
        self.number_appointments_today_label.grid(row=5, column=1, pady=(10, 15))
        self.number_appointments_today_value_label.grid(row=5, column=2, pady=(10, 15))
    
    def set_appointments_grid(self):
        """
        Sets the grid layout for the appointments sub-frame.
        """
        self.appointments_heading_label.grid(row=0, column=1, pady=(10, 0))
        self.appointments_sub_heading_label.grid(row=1, column=1, pady=(0, 10))
        self.appointments_sub_frame.grid(row=2, column=1, pady=(0, 10))
        
    def reset(self):
        """
        Resets the doctor's home page.
        """
        self.main_heading_label.configure(text=f"Willkommen, {self.get_doctor_name()}!")
        self.insurance_value_label.configure(text=self.get_treated_insurance_types())
        self.weekly_hours_value_label.configure(text=self.get_weekly_hours())
        self.number_appointments_week_value_label.configure(text=self.get_appointments_week())
        self.number_appointments_today_value_label.configure(text=self.get_appointments_day())
        self.appointments_sub_frame.reset()
        
    def get_doctor_name(self) -> str:
        """
        Retrieves the name of the doctor from a CSV file.

        Returns:
            str: The name of the doctor.
        """
        return read_csv("data/doctors.csv", index_col="Username").loc[self.data_bundle["username"]]["Name"]
    
    # csv format: [Username (str),Name (str),ID/Passwort (str),privat (boolean),gesetzlich (boolean),freiwillig gesetzlich (boolean)]
    def get_treated_insurance_types(self) -> str:
        """
        Retrieves the types of insurance the doctor treats.

        Returns:
            str: The types of insurance the doctor treats.
        """
        df = read_csv("data/doctors.csv", index_col="Username")
        username = self.data_bundle["username"]
        privat = df.loc[username]["privat"]
        gesetzlich = df.loc[username]["gesetzlich"]
        freiwillig_gesetzlich = df.loc[username]["freiwillig gesetzlich"]

        insurance_types = {
            True: {
                True: {
                    True: "Privatpatienten,\ngesetzlich Versicherte und\nfreiwillig gesetzlich Versicherte",
                    False: "Privatpatienten und\ngesetzlich Versicherte"},
                False: {
                    True: "Privatpatienten und\nfreiwillig gesetzlich Versicherte",
                    False: "Privatpatienten"}},
            False: {
                True: {
                    True: "Gesetzlich Versicherte und\nfreiwillig gesetzlich Versicherte",
                    False: "Gesetzlich Versicherte"},
                False: {
                    True: "Freiwillig gesetzlich Versicherte",
                    False: "Keine"}}
        }

        return insurance_types[privat][gesetzlich][freiwillig_gesetzlich]
            
    def get_weekly_hours(self) -> int:
        """
        Calculates the number of weekly working hours for the doctor.

        Returns:
            int: The number of weekly working hours.
        """
        mo = datetime.now() + relativedelta(weekday=MO(-1), hour=0)
        sa = mo + relativedelta(weekday=SA)
        with open("data/doctors_free.json") as file:
            data = json.load(file)
        ruleset = rruleset()
        for rulestr in data[self.data_bundle["username"]]:
            rule = rrulestr(rulestr)
            hours = range(rule._byhour[0], rule._byhour[-1])
            rule = rule.replace(dtstart=mo, byhour=hours)
            ruleset.rrule(rule)
        return len(ruleset.between(mo, sa))
    
    def get_appointments_week(self) -> int:
        """
        Calculates the number of appointments for the current week.

        Returns:
            int: The number of appointments for the current week.
        """
        next_days_in_week: list[date] = self.get_next_week_days()
        appointments = 0
        
        for day in next_days_in_week:
            appointments += self.count_appointments(day)
            
        return appointments + self.get_appointments_day()
    
    def get_appointments_day(self) -> int:
        """
        Calculates the number of appointments for the current day by counting the number
        of appointments for the current day that are later than the current time.

        Returns:
            int: The number of appointments for the current day.
        """
        df = pd.read_csv("data/appointments.csv")   # read appointments.csv
        now = datetime.now()    # get current datetime
        df["dt_start"] = df["dt_start"].apply(lambda x: datetime.strptime(x, "%d-%m-%Y %H:%M"))   # convert date string to datetime object
        if len(df) == 0:    
            return 0    # return 0 if there are no appointments
        # count appointments for the given date that are later than the current time
        count = len(df[(df["Doctor"] == self.data_bundle["username"]) & (df["dt_start"].dt.date == now.date()) & (df["dt_start"] > now)])
        return count
            
    def count_appointments(self, date: date) -> int:
        """
        Counts the number of appointments for a specific date

        Args:
            date (date): The date to count appointments for.

        Returns:
            int: The number of appointments for the specified date.
        """
        df = pd.read_csv("data/appointments.csv")   # read appointments.csv
        df["dt_start"] = df["dt_start"].apply(lambda x: datetime.strptime(x, "%d-%m-%Y %H:%M").date())   # convert date string to date object
        if len(df) == 0:
            return 0    # return 0 if there are no appointments
        count = len(df[(df["Doctor"] == self.data_bundle["username"]) & (df["dt_start"] == date)])  # count appointments for the given date
        return count
    
    def get_next_week_days(self) -> list[date]:
        """
        Retrieves the dates of the next week.

        Returns:
            list[date]: The dates of the next week.
        """
        today = date.today()
        next_days_in_week = []
        for i in range(7):
            next_day = today + timedelta(days=i)    # add i days to today
            # check if next_day is in the same week and not a weekend
            if next_day.weekday() < 5 and next_day.isocalendar()[1] == today.isocalendar()[1]:  # isocalendar()[1] returns the week number to make sure it's in the same week
                next_days_in_week.append(next_day)
        return next_days_in_week
            
    def book_appointment(self):
        """
        Books an appointment for the doctor.
        """
        self.nametowidget(".!mainsidebar").book_event()
    
