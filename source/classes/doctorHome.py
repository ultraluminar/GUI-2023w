import customtkinter as ctk
import json

import pandas as pd
from pandas import read_csv
from dateutil.rrule import rrulestr, weekday
from datetime import date, datetime, timedelta

from source.classes.customWidgets.doctorAppointmentOverview import DoctorOverview

class DoctorHome(ctk.CTkScrollableFrame):
    def __init__(self, master: ctk.CTk):
        super().__init__(master=master, corner_radius=0, fg_color="transparent")
        
        self.auth_service = self.nametowidget(".").auth_service
        self.username = None
        
        self.grid_columnconfigure(0, weight=1)
        
        print("test", self.get_appointments_day(), "test")
        
        # fonts
        font30 = ctk.CTkFont(family="Segoe UI", size=30, weight="bold")
        font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        fat = ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        
        # main widgets
        self.main_heading_label = ctk.CTkLabel(self, text=f"Willkommen, {self.username}!", font=font30)
        self.sub_heading_label = ctk.CTkLabel(self, text="Was möchten sie tun?")
        
        # profil sub Frame
        self.profil_frame = ctk.CTkFrame(self)
        self.profil_frame.grid_columnconfigure((0, 3), weight=1)
        self.profil_heading_label = ctk.CTkLabel(self.profil_frame, text="Mein Profil", font=font24)
        self.profil_sub_heading_label = ctk.CTkLabel(self.profil_frame, text="Hier können sie ihre Daten einsehen.")
        self.insurance_type_label = ctk.CTkLabel(self.profil_frame, text="Sie behandeln:", anchor="w", width=280)
        self.insurance_value_label = ctk.CTkLabel(self.profil_frame, width=110, anchor="w", font=fat)
        self.weekly_hours_label = ctk.CTkLabel(self.profil_frame, text="Arbeitszeit:", anchor="w", width=280)
        self.weekly_hours_value_label = ctk.CTkLabel(self.profil_frame, width=110, anchor="w", font=fat)
        self.number_appointments_week_label = ctk.CTkLabel(self.profil_frame, text="Anzahl anstehender Termine diese Woche:", anchor="w", width=280)
        self.number_appointments_week_value_label = ctk.CTkLabel(self.profil_frame, width=110, anchor="w", font=fat)
        self.number_appointments_today_label = ctk.CTkLabel(self.profil_frame, text="Davon Termine noch heute:", anchor="w", width=280)
        self.number_appointments_today_value_label = ctk.CTkLabel(self.profil_frame, width=110, anchor="w", font=fat)
        
        # appointments sub Frame
        self.appointments_frame = ctk.CTkFrame(self)
        self.appointments_frame.grid_columnconfigure((0, 2), weight=1)
        self.appointments_heading_label = ctk.CTkLabel(self.appointments_frame, text="Meine Termine", font=font24)
        self.appointments_sub_heading_label = ctk.CTkLabel(self.appointments_frame, text="Hier können sie ihre Termine einsehen.")
        self.appointments_sub_frame = DoctorOverview(self.appointments_frame)
        
        self.set_profile_grid()
        self.set_appointments_grid()
        self.set_main_grid()
        
    def set_main_grid(self):
        self.main_heading_label.grid(row=0, column=0, columnspan=2, pady=(10, 0), sticky="nsew")
        self.sub_heading_label.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="nsew")
        self.profil_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.appointments_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
    def set_profile_grid(self):
        self.profil_heading_label.grid(row=0, column=1, columnspan=2, pady=(10, 0))
        self.profil_sub_heading_label.grid(row=1, column=1, columnspan=2, pady=(0, 10))
        self.insurance_type_label.grid(row=2, column=1, pady=(10, 0))
        self.insurance_value_label.grid(row=2, column=2, pady=(10, 0))
        self.weekly_hours_label.grid(row=3, column=1, pady=(10, 0))
        self.weekly_hours_value_label.grid(row=3, column=2, pady=(10, 0))
        self.number_appointments_week_label.grid(row=4, column=1, pady=(10, 0))
        self.number_appointments_week_value_label.grid(row=4, column=2, pady=(10, 0))
        self.number_appointments_today_label.grid(row=5, column=1, pady=(10, 15))
        self.number_appointments_week_value_label.grid(row=5, column=2, pady=(10, 15))
    
    def set_appointments_grid(self):
        self.appointments_heading_label.grid(row=0, column=1, pady=(10, 0))
        self.appointments_sub_heading_label.grid(row=1, column=1, pady=(0, 10))
        self.appointments_sub_frame.grid(row=2, column=1, pady=(0, 10))
        
    def reset(self):
        self.username = self.auth_service.username
        self.main_heading_label.configure(text=f"Willkommen, {self.get_doctor_name()}!")
        self.insurance_value_label.configure(text=self.get_treated_insurance_types())
        self.weekly_hours_value_label.configure(text=self.get_weekly_hours())
        self.number_appointments_week_value_label.configure(text=self.get_appointments_week())
        self.number_appointments_today_value_label.configure(text=self.get_appointments_day())
        self.appointments_sub_frame.reset()
        
    def get_doctor_name(self):
        return read_csv("data/doctors.csv", index_col="username").loc[self.username]["Name"]
    
    # csv format: [Username (str),Name (str),ID/Passwort (str),privat (boolean),gesetzlich (boolean),freiwillig gesetzlich (boolean)]
    def get_treated_insurance_types(self):
        df = read_csv("data/doctors.csv", index_col="username")
        username = self.username
        privat = df.loc[username]["privat"]
        gesetzlich = df.loc[username]["gesetzlich"]
        freiwillig_gesetzlich = df.loc[username]["freiwillig gesetzlich"]
        
        if privat and gesetzlich and freiwillig_gesetzlich:
            return "Privatpatienten, gesetzlich Versicherte und freiwillig gesetzlich Versicherte"
        elif privat and gesetzlich:
            return "Privatpatienten und gesetzlich Versicherte"
        elif privat and freiwillig_gesetzlich:
            return "Privatpatienten und freiwillig gesetzlich Versicherte"
        elif gesetzlich and freiwillig_gesetzlich:
            return "Gesetzlich Versicherte und freiwillig gesetzlich Versicherte"
        elif privat:
            return "Privatpatienten"
        elif gesetzlich:
            return "Gesetzlich Versicherte"
        elif freiwillig_gesetzlich:
            return "Freiwillig gesetzlich Versicherte"
        else:
            return "Keine"
        
    def get_weekly_hours(self):
        days: list[weekday] = [weekday(i) for i in range(5)]
        hours: list[int] = [i for i in range(8, 17)]
        weekly_hours = 0
        # iterate over all weekdays and hours and check if the doctor is available
        for day in days: 
            for hour in hours:
                if self.is_in_rules(day, hour):
                    weekly_hours += 1
        return weekly_hours
    
    def get_appointments_week(self):
        next_days_in_week: list[date] = self.get_next_week_days()
        appointments = 0
        
        for day in next_days_in_week:
            appointments += self.count_appointments(day)
            
        return appointments + self.get_appointments_day()
    
    def get_appointments_day(self) -> int:
        self.username = "lösch"
        df = pd.read_csv("data/appointments.csv")   # read appointments.csv
        now = datetime.now()    # get current datetime
        df["date"] = df["date"].apply(lambda x: datetime.fromisoformat(x))   # convert date string to datetime object
        if len(df) == 0:    
            return 0    # return 0 if there are no appointments
        # count appointments for the given date that are later than the current time
        count = len(df[(df["Doctor"] == self.username) & (df["date"].dt.date == now.date()) & (df["date"] > now)])
        return count
            
    def count_appointments(self, date) -> int:
        df = pd.read_csv("data/appointments.csv")   # read appointments.csv
        df["date"] = df["date"].apply(lambda x: datetime.fromisoformat(x).date())   # convert date string to date object
        if len(df) == 0:
            return 0    # return 0 if there are no appointments
        count = len(df[(df["Doctor"] == self.username) & (df["date"] == date)])  # count appointments for the given date
        return count
    
    def get_next_week_days(self) -> list[date]:
        today = date.today()
        next_days_in_week = []
        for i in range(7):
            next_day = today + timedelta(days=i)    # add i days to today
            # Prüfen, ob der nächste Tag ein Wochentag ist (0-4 entspricht Montag bis Freitag)
            if next_day.weekday() < 5 and next_day.isocalendar()[1] == today.isocalendar()[1]:  # isocalendar()[1] returns the week number to make sure its in the same week
                next_days_in_week.append(next_day)
        return next_days_in_week

    # Check if the given weekday and hour are within the doctor's free time rules
    def is_in_rules(self, weekday: weekday, hour: int) -> bool:
        with open("data/doctors_free.json") as file:
            data = json.load(file)
        
        for rule in data[self.username]:
            rrule = rrulestr(rule)
            start_hour, end_hour = rrule.byhour[0], rrule.byhour[-1]    # byhour value pair is treated as start and end hour
            
            if weekday in rrule._byweekday and start_hour <= hour < end_hour:
                return True
        
        return False
            
    def book_appointment(self):
        self.nametowidget(".!mainsidebar").book_event()
    
