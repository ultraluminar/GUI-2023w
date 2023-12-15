import tkinter as tk
import customtkinter as ctk

from dateutil.rrule import rrule, WEEKLY, MO, TU, WE, TH, FR, SA
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta
from dataclasses import dataclass

@dataclass
class Event:
    start: datetime
    stop: datetime
    text: str

    def get_span(self):
        return (self.stop.hour - self.start.hour)*4

    def get_row(self):
        return (self.start.hour-8)*4+2

    def get_column(self):
        return self.start.weekday()

    def get_height(self):
        return

    def get_grid_args(self):
        return {
            "row": self.get_row(),
            "column": self.get_column(),
            "rowspan": self.get_span(),
            "sticky": "nswe"
        }


class WeekCalenderView(ctk.CTkFrame):
    def __init__(self, master, start_date: datetime, rule: rrule, width: int = 140, height: int = 32):
        super().__init__(master=master, width=width, height=height)

        self.start_date = start_date
        self.rule = rule
        self.day_shortnames: list[str] = ["MO", "DI", "MI", "DO", "FR"]

        self.grid_columnconfigure(list(range(0, 4+1)), weight=1)
        self.grid_rowconfigure(list(range(2, 12*4+1)), weight=1)
        
        self.start_date: datetime = self.start_date + relativedelta(weekday=MO(-1), hour=0)
        self.stop_date: datetime = self.start_date + relativedelta(weekday=SA)
        
        self.rule: rrule = self.rule.replace(dtstart=self.start_date)
        self.day_rule: rrule = self.rule.replace(byhour=8)
        
        self.events: list[datetime] = self.rule.between(after=self.start_date, before=self.stop_date)
        self.days: list[int] = [dt.day for dt in self.day_rule.between(after=self.start_date, before=self.stop_date)]

        
        # widgets
        self.day_labels: list[ctk.CTkLabel] = [ctk.CTkLabel(self, text=day) for day in self.day_shortnames]
        self.date_labels: list[ctk.CTkLabel] = [ctk.CTkLabel(self, text=str(day)) for day in self.days]
        self.event_buttons: list[list[ctk.CTkLabel]] = [[ctk.CTkLabel(self, text=f"{hour} - {hour+1} Uhr", state="disabled", fg_color="transparent") for hour in range(8, 18+1)] for _ in self.days]
        for event in self.events:
            self.event_buttons[event.weekday()][event.hour - 8].configure(state="normal", fg_color="gray")

        self.set_grid()
        start = datetime(2023, 12, 12, 10)
        stop = datetime(2023, 12, 12, 13)
        span = stop.hour-start.hour
        print(span)
        self.event0 = Event(start, stop, "POGGERS")

        self.label_event0 = ctk.CTkLabel(self, text=self.event0.text)
        self.label_event0.configure(height=self.label_event0.cget("height")*span)
        self.label_event0.grid(**self.event0.get_grid_args())

        start = datetime(2023, 12, 14, 8)
        stop = datetime(2023, 12, 14, 17)
        self.event1 = Event(start, stop, "Kiefer")
        self.label_event1 = ctk.CTkLabel(self, text=self.event1.text)
        span = stop.hour - start.hour
        self.label_event1.configure(height=self.label_event1.cget("height")*span)
        self.label_event1.grid(**self.event1.get_grid_args())

    def set_grid(self):
        for column, widget in enumerate(self.day_labels):
            widget.grid(column=column, row=0, sticky="nsew")
        for column, widget in enumerate(self.date_labels):
            widget.grid(column=column, row=1, sticky="nsew")
        for column, rows in enumerate(self.event_buttons):
            for row, widget in enumerate(rows):
                widget.grid(column=column, row=row*4+2, sticky="nsew", padx=1, pady=1, rowspan=4)
    
if __name__ == "__main__":
    CTk = ctk.CTk()
    CTk.geometry("1000x500")
    CTk.grid_columnconfigure(0, weight=1)
    CTk.grid_rowconfigure(0, weight=1)
    rule = rrule(freq=WEEKLY, byweekday=range(5), byhour=range(8, 18+1), byminute=0, bysecond=0)
    view = WeekCalenderView(CTk, start_date=datetime.today(), rule=rule)
    view.grid(column=0, row=0, sticky="nsew")
    CTk.mainloop()