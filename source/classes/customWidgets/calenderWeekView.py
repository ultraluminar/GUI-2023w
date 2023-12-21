from pathlib import Path

import customtkinter as ctk

from dateutil.rrule import rrule, WEEKLY, MO, SA, rrulestr, weekdays
from dateutil.relativedelta import relativedelta
from datetime import datetime

from source.utils import center_window
from source.classes.customWidgets.event_label import EventLabel
from source.auth_util import loadJson

path_docotrs_free = Path("data/doctors_free.json")
workdays = weekdays[:5]

class WeekCalenderView(ctk.CTkFrame):
    def __init__(self, master, width: int = 140, height: int = 32):
        super().__init__(master=master, width=width, height=height)

        self.events: list[EventLabel] = []

        self.start_3m: datetime = datetime.now().replace(hour=0)
        self.stop_3m = self.start_3m + relativedelta(months=3)

        self.start_week = None
        self.stop_week = None
        self.doctor_name = None
        self.dates = None

        self.day_shortnames: list[str] = ["MO", "DI", "MI", "DO", "FR"]

        self.grid_columnconfigure(list(range(5)), weight=1)
        self.grid_rowconfigure(list(range(2, 10*4+2)), weight=1)

        self.set_week_limits(datetime.now())

        self.date_rule = rrule(freq=WEEKLY, byweekday=range(5), byhour=8, byminute=0, bysecond=0, dtstart=self.start_week)

        # widgets
        self.day_labels: list[ctk.CTkLabel] = [ctk.CTkLabel(self, text=day) for day in self.day_shortnames]
        self.date_labels: list[ctk.CTkLabel] = [ctk.CTkLabel(self) for _ in workdays]
        self.hour_buttons: list[list[ctk.CTkLabel]] = [[
            ctk.CTkLabel(self, text=f"{hour} - {hour+1} Uhr", corner_radius=5, fg_color="gray20"
                ) for hour in range(8, 18)] for _ in workdays]

        self.update_date_labels()
        self.set_grid()

    def set_week_limits(self, day_of_week: datetime):
        self.start_week = day_of_week + relativedelta(weekday=MO(-1), hour=0)
        self.stop_week = self.start_week + relativedelta(weekday=SA)

    def set_week(self, day_of_week: datetime, doctor_name=None):
        if doctor_name is not None:
            self.doctor_name = doctor_name

        self.set_week_limits(day_of_week)
        self.update_date_labels()
        self.update_event_labels()

    def update_event_labels(self):
        self.reset()

        rule_strings = loadJson(path_docotrs_free)[self.doctor_name]
        rules = [rrulestr(rule) for rule in rule_strings]
        labels = self.labels_from_rules(rules)

        week_filter = self.get_week_filter()
        labels = [label for isday, label in zip(week_filter, labels) if isday]

        self.events.extend(labels)
        for label in self.events:
            label.grid()


    def update_date_labels(self):
        self.dates = [str(dt.day) for dt in self.date_rule.between(after=self.start_week, before=self.stop_week)]
        for date, label in zip(self.dates, self.date_labels):
            label.configure(text=date)

    def labels_from_rules(self, rules: list[rrule]):
        labels: list[EventLabel] = []

        for rule in rules:
            day_rule = rule.replace(byhour=8, dtstart=self.start_week)
            days: list[datetime] = day_rule.between(after=self.start_week, before=self.stop_week)

            labels = [EventLabel(master=self, dt_start=day, rule=rule) for day in days]
            labels.extend(labels)

        return labels

    def get_week_filter(self) -> list[bool]:
        days: rrule = rrule(freq=WEEKLY, dtstart=self.start_week, byweekday=weekdays, byhour=8)
        week: list[datetime] = days.between(after=self.start_week, before=self.stop_week)

        return [self.start_3m <= day < self.stop_3m for day in week]

    def add_ex_date(self, dt_start: datetime, dt_stop: datetime):
        label = EventLabel(master=self, dt_start=dt_start, dt_stop=dt_stop, fg_color="darkred")
        label.grid()
        self.events.append(label)

    def reset(self):
        if self.events:
            for event in self.events:
                event.label.destroy()
            self.events.clear()

    def set_grid(self):
        for row, labels in enumerate([self.day_labels, self.date_labels]):
            for column, widget in enumerate(labels):
                widget.grid(column=column, row=row, sticky="nsew")
        for column, rows in enumerate(self.hour_buttons):
            for row, widget in enumerate(rows):
                widget.grid(column=column, row=row * 4 + 2, sticky="nsew", padx=1, pady=1, rowspan=4)