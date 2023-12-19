import customtkinter as ctk
import tkinter as tk
from datetime import datetime
from dateutil.relativedelta import relativedelta, MO

from source.classes.customWidgets.calenderWeekView import WeekCalenderView

class CalenderViewFrame(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk):
        super().__init__(master=master)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # variables
        self.current: datetime = datetime.now() + relativedelta(weekday=MO(-1))
        
        # fonts
        self.font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        
        # main widgets
        self.heading_label = ctk.CTkLabel(self, text="Termin auswählen", font=self.font24)
        self.sub_heading_label = ctk.CTkLabel(self, text="Sehen sie sich den Kalender an und buchen sie einen Termin.")
        self.last_week_button = ctk.CTkButton(self, text="last", command=self.last_week)
        self.next_week_button = ctk.CTkButton(self, text="next", command=self.next_week)
        self.week_calender_view = WeekCalenderView(self)
        self.book_button = ctk.CTkButton(self, text="Buchen", command=self.booking_view)

        self.set_main_grid()
        
    def set_main_grid(self):
        self.heading_label.grid(column=1, row=0, pady=(20, 0), sticky="nsew")
        self.sub_heading_label.grid(column=1, row=1, sticky="nsew")
        self.last_week_button.grid(column=0, row=0, rowspan=2, pady=20, sticky="e", padx=(20, 0))
        self.next_week_button.grid(column=2, row=0, rowspan=2, pady=20, sticky="w", padx=(0, 20))
        self.week_calender_view.grid(column=0, columnspan=3, row=2, pady=20, sticky="nsew")
        self.book_button.grid(column=0, columnspan=3, row=3, pady=20, sticky="e", padx=(0, 20))

    def set_doctor(self, name: str):
        self.week_calender_view.set_week(doctor_name=name, day_of_week=self.current)

    def reset(self):
        self.week_calender_view.reset()
        
    def last_week(self):
        self.reset()
        self.current += relativedelta(weeks=-1)
        self.week_calender_view.set_week(day_of_week=self.current)
        pass
        
    def next_week(self):
        self.reset()
        self.current += relativedelta(weeks=1)
        self.week_calender_view.set_week(day_of_week=self.current)
        pass
    
    def booking_view(self):
        pass