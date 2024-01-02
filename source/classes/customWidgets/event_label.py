import customtkinter as ctk

from datetime import datetime, timedelta
from dateutil.rrule import rrule


class EventLabel:
    def __init__(self, master, dt_start: datetime, dt_stop: datetime = None, rule: rrule = None, fg_color=("#3ba156", "#458556")):
        self.dt_start = dt_start
        self.dt_stop = dt_stop

        if rule is not None:
            self.dt_start, self.dt_stop = [self.dt_start.replace(hour=hour) for hour in rule._byhour]

        self.column = self.dt_start.weekday() + 1
        self.row = (self.dt_start - self.dt_start.replace(hour=8)) // timedelta(minutes=15) + 4
        self.rowspan = (self.dt_stop - self.dt_start) // timedelta(minutes=15)

        self.label = ctk.CTkLabel(master=master, text="", corner_radius=5, fg_color=fg_color)

    def __str__(self):
        return f'EventLabel({self.dt_start.strftime("%d-%m-%Y %H:%M")}, {self.dt_stop.strftime("%d-%m-%Y %H:%M")})'

    def grid(self):
        self.label.grid(row=self.row, column=self.column, rowspan=self.rowspan, sticky="nsew", padx=1, pady=1)