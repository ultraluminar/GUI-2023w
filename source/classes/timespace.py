from source.classes.customWidgets.event_label import EventLabel
from datetime import time, datetime
from dateutil.relativedelta import relativedelta

class TimeSpace:
    """
    The TimeSpace class represents a time-space grid for scheduling events.

    Methods:
        __init__(self, events_free: list[EventLabel], events_used: list[EventLabel] = None):
            Initializes a TimeSpace object with the given lists of free and used events.

        get_termine(self, duration: int) -> list[list[time]]:
            Returns a list of available time slots for each weekday, based on the given duration.
    """

    def __init__(self, events_free: list[EventLabel], events_used: list[EventLabel] = None):
        """
        Initializes a TimeSpace object with the given lists of free and used events.

        Args:
            events_free (list[EventLabel]): A list of free events.
            events_used (list[EventLabel], optional): A list of used events. Defaults to None.
        """
        self.quaters_free: list[set[time]] = [set() for _ in range(5)]
        self.quaters_used: list[set[time]] = [set() for _ in range(5)]

        for event in events_free:
            quarters = {(event.dt_start + relativedelta(minutes=15*quarter)).time() for quarter in range(event.rowspan+1)}
            self.quaters_free[event.dt_start.weekday()] |= quarters

        for event in events_used:
            quarters = {(event.dt_start + relativedelta(minutes=15*quarter)).time() for quarter in range(event.rowspan)}
            self.quaters_used[event.dt_start.weekday()] |= quarters

    def get_termine(self, duration: int) -> list[list[time]]:
        """
        Returns a list of available time slots for each weekday, based on the given duration.

        Args:
            duration (int): The duration of the time slots in minutes.

        Returns:
            list[list[time]]: A list of available time slots for each weekday.
        """
        termine: list[list[time]] = [[] for _ in range(5)]
        for weekday, quaters in enumerate(self.quaters_free):
            for start in quaters:

                hour1, minute1 = divmod(duration, 4)
                hour2, minute = divmod(start.minute + minute1 * 15, 60)
                hour = start.hour + hour1 + hour2

                stop = time(hour=hour, minute=minute)
                if stop in self.quaters_free[weekday] and not any(start <= q < stop for q in self.quaters_used[weekday]):
                    termine[weekday].append(start)
            termine[weekday].sort()
        return termine