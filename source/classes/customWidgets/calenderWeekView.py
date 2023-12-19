import customtkinter as ctk

from dateutil.rrule import rrule, WEEKLY, MO, TU, WE, TH, FR, SA, rrulestr
from dateutil.relativedelta import relativedelta
from datetime import datetime, time, timedelta, date
from json import load

from source.utils import center_window


class EventLabel:
    def __init__(self, master, dt_start: datetime, dt_stop: datetime = None, rule: rrule = None):
        self.dt_start = dt_start
        self.dt_stop = dt_stop

        if rule is not None:
            self.dt_start, self.dt_stop = [self.dt_start.replace(hour=hour) for hour in rule._byhour]


        self.column = self.dt_start.weekday()
        self.row = (self.dt_start - self.dt_start.replace(hour=8)) // timedelta(minutes=15) + 2
        self.rowspan = (self.dt_stop - self.dt_start) // timedelta(minutes=15)

        self.label = ctk.CTkLabel(master=master, text="text", corner_radius=5, fg_color="gray")

    def grid(self):
        self.label.grid(row=self.row, column=self.column, rowspan=self.rowspan, sticky="nsew", padx=1, pady=1)

    def destroy(self):
        self.label.destroy()


def eventlabels_from_availability(master, rules: list[rrule], dt_start: datetime) -> list[EventLabel]:
    events: list[EventLabel] = []
    dt_stop = dt_start + relativedelta(weekday=SA)
    for rule in rules:
        days: list[datetime] = rule.replace(byhour=8, dtstart=dt_start).between(after=dt_start, before=dt_stop)
        events.extend([EventLabel(master=master, dt_start=day, rule=rule) for day in days])
    return events


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

    def add_availabilities(self, rules: list[rrule], dt_start: datetime):
        self.events.extend(eventlabels_from_availability(master=self, rules=rules, dt_start=dt_start))

    def grid_events(self):
        for eventlabel in self.events:
            eventlabel.grid()

    def set_grid(self):
        for column, widget in enumerate(self.day_labels):
            widget.grid(column=column, row=0, sticky="nsew")
        for column, widget in enumerate(self.date_labels):
            widget.grid(column=column, row=1, sticky="nsew")
        for column, rows in enumerate(self.hour_buttons):
            for row, widget in enumerate(rows):
                widget.grid(column=column, row=row * 4 + 2, sticky="nsew", padx=1, pady=1, rowspan=4)




if __name__ == "__main__":
    with open("data/doctors_free.json") as file:
        data = load(file)

    dt_start = datetime.now() + relativedelta(weekday=MO(-1), hour=0)

    for doctor, rule_strings in data.items():
        CTk = ctk.CTk()
        CTk.title(doctor)
        center_window(CTk, 750, 500)

        CTk.grid_columnconfigure(0, weight=1)
        CTk.grid_rowconfigure(0, weight=1)

        view = WeekCalenderView(CTk)
        view.grid(column=0, row=0, sticky="nsew")

        rules = [rrulestr(rule).replace(dtstart=dt_start) for rule in rule_strings]
        view.add_availabilities(rules=rules, dt_start=dt_start)
        view.grid_events()

        CTk.mainloop()

