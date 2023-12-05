from dateutil.rrule import rrule, rrulestr, weekday, WEEKLY, MO, TU, WE, TH, FR
from dateutil.relativedelta import relativedelta
from datetime import datetime, time

today = datetime.today() + relativedelta(weekday=MO(+1))
in_a_week = today + relativedelta(weeks=1)
woche = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]


rule = rrule(freq=WEEKLY, byweekday=(MO, TU, WE, TH, FR), byhour=(8, 9, 10, 11, 12), byminute=0, bysecond=0)
date_list: list[datetime] = rule.between(after=today, before=in_a_week)

#for date in date_list:
#    print(f"am {woche[date.weekday()]:>10} um {date.time()} Uhr")

from source.classes.authentication_service import appendJson

appendJson("data/data_doctors.json", {"balls":  3})