from pathlib import Path

import customtkinter as ctk

from dateutil.rrule import rrule, WEEKLY, MO, SA, rrulestr
from dateutil.relativedelta import relativedelta
from datetime import datetime
from json import load

from source.utils import center_window
from source.classes.customWidgets.event_label import EventLabel
from source.auth_util import loadJson

path_docotrs_free = Path("data/doctors_free.json")

class WeekCalenderView(ctk.CTkFrame):
    def __init__(self, master, width: int = 140, height: int = 32):
        super().__init__(master=master, width=width, height=height)

        self.events: list[EventLabel] = []

        self.day_shortnames: list[str] = ["MO", "DI", "MI", "DO", "FR"]

        self.grid_columnconfigure(list(range(5)), weight=1)
        self.grid_rowconfigure(list(range(2, 10*4+3)), weight=1)


        self.start_date: datetime = datetime.now() + relativedelta(weekday=MO(-1), hour=0)
        self.stop_date: datetime = self.start_date + relativedelta(weekday=SA)

        self.rule = rrule(freq=WEEKLY, byweekday=range(5), byhour=8, byminute=0, bysecond=0, dtstart=self.start_date)
        self.dates: list[str] = [str(dt.day) for dt in self.rule.between(after=self.start_date, before=self.stop_date)]

        # widgets
        self.day_labels: list[ctk.CTkLabel] = [ctk.CTkLabel(self, text=day) for day in self.day_shortnames]
        self.date_labels: list[ctk.CTkLabel] = [ctk.CTkLabel(self, text=day) for day in self.dates]
        self.hour_buttons: list[list[ctk.CTkLabel]] = [[
            ctk.CTkLabel(self, text=f"{hour} - {hour+1} Uhr", corner_radius=5, fg_color="gray20"
                ) for hour in range(8, 18)] for _ in self.dates]

        self.set_grid()

    def add_availabilities(self, doctor_name: str, dt_start: datetime):
        rule_strings = loadJson(path_docotrs_free)[doctor_name]
        rules = [rrulestr(rule).replace(dtstart=dt_start) for rule in rule_strings]
        events: list[EventLabel] = []
        dt_stop = dt_start + relativedelta(weekday=SA)
        for rule in rules:
            days: list[datetime] = rule.replace(byhour=8, dtstart=dt_start).between(after=dt_start, before=dt_stop)
            events.extend([EventLabel(master=self, dt_start=day, rule=rule) for day in days])

        self.events.extend(events)
        self.grid_events()

    def reset(self):
        if self.events:
            for event in self.events:
                event.label.destroy()
            self.events.clear()

    def grid_events(self):
        for eventlabel in self.events:
            eventlabel.grid()

    def set_grid(self):
        for row, labels in enumerate([self.day_labels, self.date_labels]):
            for column, widget in enumerate(labels):
                widget.grid(column=column, row=row, sticky="nsew")
        for column, rows in enumerate(self.hour_buttons):
            for row, widget in enumerate(rows):
                widget.grid(column=column, row=row * 4 + 2, sticky="nsew", padx=1, pady=1, rowspan=4)


if __name__ == "__main__":
    names = loadJson(path_docotrs_free)

    dt_start = datetime.now() + relativedelta(weekday=MO(-1), hour=0)

    for name in names:
        CTk = ctk.CTk()
        CTk.title(name)
        center_window(CTk, 750, 500)

        CTk.grid_columnconfigure(0, weight=1)
        CTk.grid_rowconfigure(0, weight=1)

        view = WeekCalenderView(CTk)
        view.grid(column=0, row=0, sticky="nsew")

        view.add_availabilities(doctor_name=name, dt_start=dt_start)
        CTk.mainloop()

