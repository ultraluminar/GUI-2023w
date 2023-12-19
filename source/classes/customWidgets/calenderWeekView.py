import customtkinter as ctk

from dateutil.rrule import rrule, WEEKLY, MO, TU, WE, TH, FR, SA
from dateutil.relativedelta import relativedelta
from datetime import datetime, time, timedelta, date

from source.utils import center_window

class EventList:
    def __init__(self, master, rules: list[rrule]):
        self.events: list[Event] = []
        for rule in rules:
            for weekday in rule._byweekday:
                event = Event(master=master, rule=rule, d_start=datetime.today().replace(day=11+weekday))
                event.grid()
                self.events.append(event)


class Event:
    def __init__(self, master, dt_start: datetime = None, dt_stop: datetime = None, rule: rrule = None, d_start: date = None):
        self.dt_start = dt_start
        self.dt_stop = dt_stop

        if rule is not None:
            self.dt_start, self.dt_stop = [datetime.combine(d_start, time(hour=hour)) for hour in rule._byhour]


        self.column = self.dt_start.weekday()
        self.row = (self.dt_start - self.dt_start.replace(hour=8)) // timedelta(minutes=15) + 2
        self.rowspan = (self.dt_stop - self.dt_start) // timedelta(minutes=15)

        self.label = ctk.CTkLabel(master=master, text="text", corner_radius=5, fg_color="gray")

    def grid(self):
        self.label.grid(row=self.row, column=self.column, rowspan=self.rowspan, sticky="nsew", padx=1, pady=1)


class WeekCalenderView(ctk.CTkFrame):
    def __init__(self, master, start_date: datetime, rule: rrule, width: int = 140, height: int = 32):
        super().__init__(master=master, width=width, height=height)

        self.start_date = start_date
        self.rule = rule
        self.day_shortnames: list[str] = ["MO", "DI", "MI", "DO", "FR"]

        self.grid_columnconfigure(list(range(5)), weight=1)
        self.grid_rowconfigure(list(range(2, 12*4+1)), weight=1)

        self.hour_labels()

        rules = [
            rrule(freq=WEEKLY, byweekday=(MO, WE, TH), byhour=(10, 13)),
            rrule(freq=WEEKLY, byweekday=(TU, FR), byhour=(14, 16), byminute=(15, 15))
        ]
        self.events = EventList(self, rules)

        start = datetime(2023, 12, 13, 12)
        stop = datetime(2023, 12, 13, 15, 45)

        e = Event(self, dt_start=start, dt_stop=stop)
        e.grid()
        e2 = Event(self, d_start=datetime.today().replace(day=14), rule=rules[0])
        e2.grid()

    def hour_labels(self):
        start_date: datetime = self.start_date + relativedelta(weekday=MO(-1), hour=0)
        stop_date: datetime = start_date + relativedelta(weekday=SA)
        
        rule: rrule = self.rule.replace(dtstart=start_date)
        day_rule: rrule = rule.replace(byhour=8)
        
        events: list[datetime] = rule.between(after=start_date, before=stop_date)
        days: list[int] = [dt.day for dt in day_rule.between(after=start_date, before=stop_date)]

        
        # widgets
        day_labels: list[ctk.CTkLabel] = [ctk.CTkLabel(self, text=day) for day in self.day_shortnames]
        date_labels: list[ctk.CTkLabel] = [ctk.CTkLabel(self, text=str(day)) for day in days]
        event_buttons: list[list[ctk.CTkLabel]] = [[
            ctk.CTkLabel(self, text=f"{hour} - {hour+1} Uhr", corner_radius=5, fg_color="transparent"
                ) for hour in range(8, 18+1)
            ] for _ in days
        ]
        for event in events:
            event_buttons[event.weekday()][event.hour - 8].configure(state="normal", fg_color="gray20")

        for column, widget in enumerate(day_labels):
            widget.grid(column=column, row=0, sticky="nsew")
        for column, widget in enumerate(date_labels):
            widget.grid(column=column, row=1, sticky="nsew")
        for column, rows in enumerate(event_buttons):
            for row, widget in enumerate(rows):
                widget.grid(column=column, row=row * 4 + 2, sticky="nsew", padx=1, pady=1, rowspan=4)



    
if __name__ == "__main__":
    CTk = ctk.CTk()

    center_window(CTk, 750, 500)

    CTk.grid_columnconfigure(0, weight=1)
    CTk.grid_rowconfigure(0, weight=1)

    rule = rrule(freq=WEEKLY, byweekday=range(5), byhour=range(8, 18+1), byminute=0, bysecond=0)
    view = WeekCalenderView(CTk, start_date=datetime.today(), rule=rule)
    view.grid(column=0, row=0, sticky="nsew")

    CTk.mainloop()