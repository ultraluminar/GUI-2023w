import customtkinter as ctk
import tkinter as tk
from datetime import datetime
from dateutil.relativedelta import relativedelta, MO
from dateutil.rrule import rrule, WEEKLY

from source.classes.customWidgets.calenderWeekView import WeekCalenderView
from source.classes.booking import Booking

class CalenderViewFrame(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk):
        super().__init__(master=master)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # variables
        self.min = None
        self.max = None
        self.current = None
        
        # fonts
        self.font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        
        # main widgets
        self.heading_label = ctk.CTkLabel(self, text="Termin auswählen", font=self.font24)
        self.sub_heading_label = ctk.CTkLabel(self, text="Sehen sie sich den Kalender an und buchen sie einen Termin.")
        self.last_week_button = ctk.CTkButton(self, text="last", command=lambda: self.update_current(weeks=-1))
        self.next_week_button = ctk.CTkButton(self, text="next", command=lambda: self.update_current(weeks=1))
        self.week_calender_view = WeekCalenderView(self)
        self.booking = None
        self.book_button = ctk.CTkButton(self, text="Buchen", command=self.booking_view)
        self.buttons = [self.last_week_button, self.next_week_button]

        self.set_main_grid()
        
    def set_main_grid(self):
        self.heading_label.grid(column=1, row=0, pady=(20, 0), sticky="nsew")
        self.sub_heading_label.grid(column=1, row=1, sticky="nsew")
        self.last_week_button.grid(column=0, row=0, rowspan=2, pady=20, sticky="e", padx=(20, 0))
        self.next_week_button.grid(column=2, row=0, rowspan=2, pady=20, sticky="w", padx=(0, 20))
        self.week_calender_view.grid(column=0, columnspan=3, row=2, pady=20, sticky="nsew")
        self.book_button.grid(column=0, columnspan=3, row=3, pady=20, sticky="e", padx=(0, 20))

    def update_current(self, weeks: int = None, name: str = None):
        if weeks is None:
            self.min = datetime.now() + relativedelta(weekday=MO(-1), hour=0)
            self.max = self.min + relativedelta(months=3)
            self.current = self.min
            weeks = 0

        new = self.current + relativedelta(weeks=weeks)
        states = ["normal", "normal"]
        if new < self.min:
            states[0] = "disabled"
        elif new > self.max:
            states[1] = "disabled"
        else:
            self.current = new
            self.week_calender_view.set_week(doctor_name=name, day_of_week=self.current)

        for button, state in zip(self.buttons, states):
            button.configure(state=state)


    def set_doctor(self, name: str = None):
        self.update_current(name=name)

    def reset(self):
        pass
        
    def last_week(self):
        self.current += relativedelta(weeks=-1)
        self.week_calender_view.set_week(day_of_week=self.current)
        
    def next_week(self):
        self.current += relativedelta(weeks=1)
        self.week_calender_view.set_week(day_of_week=self.current)
    
    def booking_view(self):
        if self.booking is None or not self.booking.winfo_exists():
            self.booking = Booking()    # create window if its None or destroyed
        elif self.booking.state() == "iconic":
            self.booking.deiconify()    # bring back window if its minimized
        else:
            self.booking.focus()