import tkinter as tk
import customtkinter as ctk

from dateutil.rrule import rrule, WEEKLY, MO, TU, WE, TH, FR, SA
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta

class WeekCalenderView(ctk.CTkFrame):
    def __init__(self, master, start_date: datetime, rule: rrule, width: int = 140, height: int = 32):
        super().__init__(master=master, width=width, height=height)

        self.start_date = start_date
        self.rule = rule
        self.day_shortnames: list[str] = ["MO", "DI", "MI", "DO", "FR"]

        self.grid_columnconfigure(list(range(0, 4+1)), weight=1)
        self.grid_rowconfigure(list(range(2, 12+1)), weight=1)
        
        self.start_date: datetime = self.start_date + relativedelta(weekday=MO(-1), hour=0)
        self.stop_date: datetime = self.start_date + relativedelta(weekday=SA)
        
        self.rule: rrule = self.rule.replace(dtstart=self.start_date)
        self.day_rule: rrule = self.rule.replace(byhour=8)
        
        self.events: list[datetime] = self.rule.between(after=self.start_date, before=self.stop_date)
        self.days: list[int] = [dt.day for dt in self.day_rule.between(after=self.start_date, before=self.stop_date)]

        
        # widgets
        self.day_labels: list[ctk.CTkLabel] = [ctk.CTkLabel(self, text=day) for day in self.day_shortnames]
        self.date_labels: list[ctk.CTkLabel] = [ctk.CTkLabel(self, text=str(day)) for day in self.days]
        self.event_buttons: list[list[ctk.CTkButton]] = [[ctk.CTkButton(self, text="", state="disabled") for _ in range(8, 18+1)] for _ in self.days]
        
        
        self.set_grid()

    def set_grid(self):
        for column, widget in enumerate(self.day_labels):
            widget.grid(column=column, row=0, sticky="nsew")
        for column, widget in enumerate(self.date_labels):
            widget.grid(column=column, row=1, sticky="nsew")
        for column, rows in enumerate(self.event_buttons):
            for row, widget in enumerate(rows, start=2):
                widget.grid(column=column, row=row, sticky="nsew")
    
if __name__ == "__main__":
    CTk = ctk.CTk()
    CTk.grid_columnconfigure(0, weight=1)
    CTk.grid_rowconfigure(0, weight=1)
    rule = rrule(freq=WEEKLY, byweekday=(MO, TU, WE, TH, FR), byhour=(8, 9, 10, 11, 12), byminute=0, bysecond=0)
    view = WeekCalenderView(CTk, start_date=datetime.today(), rule=rule)
    view.grid(column=0, row=0, sticky="nsew")
    CTk.mainloop()