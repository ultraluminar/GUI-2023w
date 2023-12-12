from pathlib import Path

from dateutil.rrule import rrule, WEEKLY, MO, TU, WE, TH, FR
from dateutil.relativedelta import relativedelta
from datetime import datetime

today = datetime.today() + relativedelta(weekday=MO(+1)) - relativedelta(weeks=1)
in_a_week = today + relativedelta(weeks=1)
woche = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]


rule = rrule(freq=WEEKLY, byweekday=(MO, TU, WE, TH, FR), byhour=(8, 9, 10, 11, 12), byminute=0, bysecond=0)
date_list: list[datetime] = rule.between(after=today, before=in_a_week)

#for date in date_list:
#    print(f"am {woche[date.weekday()]:>10} um {date.time()} Uhr")

from pyotp import TOTP, random_base32
from source.auth_util import updateJson

updateJson(Path("data/otp_token.json"), {"token": random_base32()}, replace=True)
