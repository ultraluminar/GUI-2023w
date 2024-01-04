import customtkinter as ctk

from datetime import datetime, timedelta
from dateutil.rrule import rrule

class EventLabel:
    """
    A custom widget representing an event label in a GUI.

    Args:
        master: The parent widget.
        dt_start (datetime): The start datetime of the event.
        dt_stop (datetime, optional): The stop datetime of the event. Defaults to None.
        rule (rrule, optional): The recurrence rule for the event. Defaults to None.
        fg_color (tuple, optional): The foreground color of the label. Defaults to ("#3ba156", "#458556").

    Attributes:
        dt_start (datetime): The start datetime of the event.
        dt_stop (datetime): The stop datetime of the event.
        column (int): The column index in the grid.
        row (int): The row index in the grid.
        rowspan (int): The number of rows the label spans.
        label (CTkLabel): The label widget.

    Methods:
        grid(): Places the label widget in the grid.

    Example:
        label = EventLabel(master, datetime(2023, 1, 1, 10, 0), datetime(2023, 1, 1, 12, 0))
        label.grid()
    """

    def __init__(self, master, dt_start: datetime, dt_stop: datetime = None, rule: rrule = None, fg_color=("#3ba156", "#458556")):
        self.dt_start = dt_start
        self.dt_stop = dt_stop

        # if a rule exists, replace the start and stop datetimes with the rule datetimes
        if rule is not None:
            self.dt_start, self.dt_stop = [self.dt_start.replace(hour=hour) for hour in rule._byhour]

        self.column = self.dt_start.weekday() + 1
        self.row = (self.dt_start - self.dt_start.replace(hour=8, minute=0)) // timedelta(minutes=15) + 4
        self.rowspan = (self.dt_stop - self.dt_start) // timedelta(minutes=15)

        # label
        self.label = ctk.CTkLabel(master=master, text="", corner_radius=5, fg_color=fg_color)

    def __str__(self):
        return f'EventLabel({self.dt_start.strftime("%d-%m-%Y %H:%M")}, {self.dt_stop.strftime("%d-%m-%Y %H:%M")})'

    def grid(self):
        """
        Places the label widget in the grid.
        """
        self.label.grid(row=self.row, column=self.column, rowspan=self.rowspan, sticky="nsew", padx=1, pady=1)