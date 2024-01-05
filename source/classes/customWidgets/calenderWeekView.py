from pathlib import Path

import customtkinter as ctk

from dateutil.rrule import rrule, WEEKLY, MO, SA, rrulestr, weekdays
from dateutil.relativedelta import relativedelta
from datetime import datetime
from pandas import read_csv

from source.classes.customWidgets.event_label import EventLabel
from source.auth_util import loadJson

path_docotrs_free = Path("data/doctors_free.json")
workdays = weekdays[:5]

class WeekCalenderView(ctk.CTkFrame):
    """
    A custom calendar week view widget.

    Methods:
        set_week_limits(day_of_week: datetime): Sets the start and stop dates of the current week based on the given day of the week.
        set_week(day_of_week: datetime): Sets the current week based on the given day of the week.
        update_ex_dates(): Updates the excluded dates based on the appointments data.
        update_event_labels(): Updates the event labels based on the rules and filters.
        update_date_labels(): Updates the date labels based on the current week.
        update_month_week_label(): Updates the month and week labels based on the current week.
        labels_from_rules(rules: list[rrule]): Generates event labels based on the given rules.
        get_week_filter() -> list[bool]: Generates a week filter based on the current week and the 3-month period.
        add_ex_date(dt_start: datetime, dt_stop: datetime, fg_color: str = "darkred"): Adds an excluded date label to the calendar.
        reset(): Resets the calendar by removing all event labels.
        set_grid(): Sets the grid layout for the calendar.
    """

    def __init__(self, master, bundle: dict, width: int = 140, height: int = 32):
        """
        Initializes the WeekCalenderView.

        Args:
            master: The parent widget.
            bundle (dict): A bundle of data.
            width (int): The width of the widget.
            height (int): The height of the widget.
        """
        super().__init__(master=master, width=width, height=height)

        self.events_free: list[EventLabel] = []
        self.events_used: list[EventLabel] = []

        self.start_3m: datetime = datetime.now().replace(hour=0)
        self.stop_3m = self.start_3m + relativedelta(months=3)

        self.start_week = None
        self.stop_week = None
        self.dates = None
        self.data_bundle = bundle

        self.day_shortnames: list[str] = ["MO", "DI", "MI", "DO", "FR"]

        self.grid_columnconfigure(list(range(1, 6)), weight=1)
        self.grid_rowconfigure(list(range(2, 11*4+2)), weight=1)

        self.set_week_limits(datetime.now())

        self.date_rule = rrule(freq=WEEKLY, byweekday=range(5), byhour=8, byminute=0, bysecond=0, dtstart=self.start_week)

        # widgets
        self.month_label = ctk.CTkLabel(self, fg_color=("gray70", "gray30"), width=100)
        self.week_label = ctk.CTkLabel(self, fg_color=("gray70", "gray30"))
        self.time_labels: list[ctk.CTkLabel] = [ctk.CTkLabel(self, fg_color=("gray80", "gray20"), text=f"{time}:00") for time in range(8, 18+1)]
        self.day_labels: list[ctk.CTkLabel] = [ctk.CTkLabel(self, fg_color=("gray70", "gray30"), text=day) for day in self.day_shortnames]
        self.date_labels: list[ctk.CTkLabel] = [ctk.CTkLabel(self, fg_color=("gray70", "gray30")) for _ in workdays]
        self.hour_buttons: list[list[ctk.CTkLabel]] = [[
            ctk.CTkLabel(self, text="", corner_radius=5, fg_color=("gray75", "gray25")
                ) for _ in range(8, 18)] for _ in workdays]

        self.update_date_labels()
        self.update_month_week_label()
        self.set_grid()

    def set_week_limits(self, day_of_week: datetime):
        """
        Sets the start and stop dates of the current week based on the given day of the week.

        Args:
            day_of_week (datetime): The day of the week.
        """
        self.start_week = day_of_week + relativedelta(weekday=MO(-1), hour=0)
        self.stop_week = self.start_week + relativedelta(weekday=SA)

    def set_week(self, day_of_week: datetime):
        """
        Sets the current week based on the given day of the week and updates the calendar.

        Args:
            day_of_week (datetime): The day of the week.
        """
        self.set_week_limits(day_of_week)
        self.update_date_labels()
        self.update_event_labels()
        self.update_ex_dates()
        self.update_month_week_label()

    def update_ex_dates(self):
        """
        Updates the excluded dates based on the appointments data.
        """
        df_appointments = read_csv("data/appointments.csv")
        df_appointments = df_appointments.loc[df_appointments["Doctor"] == self.data_bundle["doctor"]]
        # iterate over all appointments get the start and stop datetimes
        for _, row in df_appointments.iterrows():
            start = datetime.strptime(row["dt_start"], "%d-%m-%Y %H:%M")
            stop = datetime.strptime(row["dt_stop"], "%d-%m-%Y %H:%M")
            # if the appointment is within the 3-month period
            if max(self.start_3m, self.start_week) <= start < min(self.stop_3m, self.stop_week):
                # add it as an excluded date
                self.add_ex_date(start, stop)

    def update_event_labels(self):
        """
        Updates the event labels based on the rules and filters.
        """
        self.reset()

        # get the recurrence rules for the doctor
        rule_strings = loadJson(path_docotrs_free)[self.data_bundle["doctor"]]
        rules = [rrulestr(rule) for rule in rule_strings]
        labels = self.labels_from_rules(rules)

        week_filter = self.get_week_filter()
        labels = [label for isday, label in zip(week_filter, labels) if isday]

        self.events_free.extend(labels)
        for label in self.events_free:
            label.grid()

        for label in self.events_used:
            label.grid()

    def update_date_labels(self):
        """
        Updates the date labels based on the current week.
        """
        self.dates = [str(dt.day) for dt in self.date_rule.between(after=self.start_week, before=self.stop_week)]
        for date, label in zip(self.dates, self.date_labels):
            label.configure(text=date)
            
    def update_month_week_label(self):
        """
        Updates the month and week labels based on the current week.
        """
        self.month_label.configure(text=self.start_week.strftime("%b %Y"))
        self.week_label.configure(text=f"KW {self.start_week.isocalendar()[1]}")

    def labels_from_rules(self, rules: list[rrule]):
        """
        Generates event labels based on the given rules.

        Args:
            rules (list[rrule]): A list of recurrence rules.

        Returns:
            list[EventLabel]: A list of event labels.
        """
        labels: list[EventLabel] = []

        # iterate over all rules
        for rule in rules:
            day_rule = rule.replace(byhour=8, dtstart=self.start_week)  # replace the hour with 8 (start of day) and set the start date to the start of the week
            days: list[datetime] = day_rule.between(after=self.start_week, before=self.stop_week)   # get all days within the week as datetimes

            labels = [EventLabel(master=self, dt_start=day, rule=rule) for day in days]  # generate event labels for each day
            labels.extend(labels)   # add the labels to the list

        return labels

    def get_week_filter(self) -> list[bool]:
        """
        Generates a week filter based on the current week and the 3-month period.

        Returns:
            list[bool]: A list of boolean values indicating whether each day is within the 3-month period.
        """
        days: rrule = rrule(freq=WEEKLY, dtstart=self.start_week, byweekday=weekdays, byhour=8) # get all days in the current week in a recurrence rule
        week: list[datetime] = days.between(after=self.start_week, before=self.stop_week)       # get all days in the current week as datetimes

        return [self.start_3m <= day < self.stop_3m for day in week]    # return a list of boolean values indicating whether each day is within the 3-month period

    def add_ex_date(self, dt_start: datetime, dt_stop: datetime, fg_color: str = "darkred"):
        """
        Adds an excluded date label to the calendar.

        Args:
            dt_start (datetime): The start date and time of the excluded date.
            dt_stop (datetime): The stop date and time of the excluded date.
            fg_color (str): The foreground color of the label.
        """
        label = EventLabel(master=self, dt_start=dt_start, dt_stop=dt_stop, fg_color=fg_color)
        label.grid()
        self.events_used.append(label)

    def reset(self):
        """
        Resets the calendar by removing all event labels.
        """
        for events in [self.events_used, self.events_free]:
            if events:
                for event in events:
                    event.label.destroy()
                events.clear()

    def set_grid(self):
        """
        Sets the grid layout for the calendar.
        """
        self.month_label.grid(column=0, row=0, sticky="nsew")
        self.week_label.grid(column=0, row=1, sticky="nsew")
        self.time_labels[0].grid(column=0, row=2, sticky="nsew", padx=1, pady=1, rowspan=4)
        self.time_labels[-1].grid(column=0, row=9 * 4 + 6, sticky="nsew", padx=1, pady=1, rowspan=4)
        # grid time labels on the left
        for row, label in enumerate(self.time_labels[1:-1]):
            label.grid(column=0, row=row * 4 + 6, sticky="nsew", rowspan=4, padx=1, pady=1)
        # grid day labels on the top
        for row, labels in enumerate([self.day_labels, self.date_labels]):
            for column, widget in enumerate(labels, start=1):
                widget.grid(column=column, row=row, sticky="nsew")
        # grid hour labels in the main table
        for column, rows in enumerate(self.hour_buttons, start=1):
            for row, widget in enumerate(rows):
                widget.grid(column=column, row=row * 4 + 4, sticky="nsew", padx=1, pady=1, rowspan=4)