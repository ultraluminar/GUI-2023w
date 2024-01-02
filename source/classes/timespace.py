from source.classes.customWidgets.event_label import EventLabel
from datetime import time
from dateutil.relativedelta import relativedelta

class TimeSpace:
    def __init__(self, events_free: list[EventLabel], events_used: list[EventLabel] = None):
        self.quaters_free: list[set[time]] = [set() for _ in range(5)]
        self.quaters_used: list[set[time]] = [set() for _ in range(5)]

        for event in events_free:
            quarters = {(event.dt_start + relativedelta(minutes=15*quarter)).time() for quarter in range(event.rowspan+1)}
            self.quaters_free[event.dt_start.weekday()] |= quarters

        for event in events_used:
            quarters = {(event.dt_start + relativedelta(minutes=15*quarter)).time() for quarter in range(event.rowspan)}
            self.quaters_used[event.dt_start.weekday()] |= quarters

    def get_termine(self, duration: int):
        print(sorted(self.quaters_free[0]))
        print(sorted(self.quaters_used[0]))
        termine: list[list[time]] = [[] for _ in range(5)]
        for weekday, quaters in enumerate(self.quaters_free):
            for start in quaters:
                hour, minute = divmod(duration, 4)
                stop = time(hour=start.hour + hour, minute=start.minute + minute)
                if stop in self.quaters_free[weekday] and not any(start <= q < stop for q in self.quaters_used[weekday]):
                    termine[weekday].append(start)
            termine[weekday].sort()
        return termine