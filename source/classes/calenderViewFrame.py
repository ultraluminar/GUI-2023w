import customtkinter as ctk
import tkinter as tk
from datetime import datetime
from dateutil.relativedelta import relativedelta, MO
from dateutil.rrule import rrule, WEEKLY

from source.auth_util import appendCSV, paths
from source.classes.timespace import TimeSpace
from source.classes.customWidgets.calenderWeekView import WeekCalenderView
from source.classes.booking import Booking

class CalenderViewFrame(ctk.CTkFrame):
    def __init__(self, master, bundle: dict):
        super().__init__(master=master)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # variables
        self.min = None
        self.max = None
        self.current = None
        self.data_bundle = bundle
        
        # fonts
        self.font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        
        # main widgets
        self.heading_label = ctk.CTkLabel(self, text="Termin auswählen", font=self.font24)
        self.sub_heading_label = ctk.CTkLabel(self, text="Sehen sie sich den Kalender an und buchen sie einen Termin.")
        self.last_week_button = ctk.CTkButton(self, text="last", command=lambda: self.update_current(weeks=-1))
        self.next_week_button = ctk.CTkButton(self, text="next", command=lambda: self.update_current(weeks=1))
        self.week_calender_view = WeekCalenderView(self, self.data_bundle)
        self.booking = None
        self.book_button = ctk.CTkButton(self, text="Buchen", command=self.booking_view)
        self.next_button = ctk.CTkButton(self, text="Weiter", command=self.next_page, state="disabled")
        self.buttons = [self.last_week_button, self.next_week_button]

        self.set_main_grid()
        
    def set_main_grid(self):
        self.heading_label.grid(column=1, row=0, pady=(20, 0), sticky="nsew")
        self.sub_heading_label.grid(column=1, row=1, sticky="nsew")
        self.last_week_button.grid(column=0, row=0, rowspan=2, pady=20, sticky="e", padx=(20, 0))
        self.next_week_button.grid(column=2, row=0, rowspan=2, pady=20, sticky="w", padx=(0, 20))
        self.week_calender_view.grid(column=0, columnspan=3, row=2, pady=20, sticky="nsew")
        self.book_button.grid(column=0, columnspan=3, row=3, pady=(0, 20), sticky="e", padx=(0, 20 + 140 + 10))
        self.next_button.grid(column=0, columnspan=3, row=3, pady=(0, 20), sticky="e", padx=(0, 20))

    def update_current(self, weeks: int = None):
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
            self.week_calender_view.set_week(day_of_week=self.current)

        for button, state in zip(self.buttons, states):
            button.configure(state=state)


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
            timespace = TimeSpace(self.week_calender_view.events_free, self.week_calender_view.events_used)
            self.booking = Booking(timespace, self.current, self.data_bundle)    # create window if its None or destroyed
        elif self.booking.state() == "iconic":
            self.booking.deiconify()    # bring back window if its minimized
        else:
            self.booking.focus()
            
    def booking_saved(self):
        # change button text to "Termin ändern"
        self.book_button.configure(text="Termin ändern", fg_color=("#26a31d", "#369130"), hover_color=("#1d8017", "#2c7527"))
        # grid next button
        self.next_button.configure(state="normal")
        
    def next_page(self):
        self.master.next_page()
        appendCSV(paths["appointments"], self.data_bundle["appointment_row"])
        