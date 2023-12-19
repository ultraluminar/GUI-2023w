from typing import Literal
from datetime import time, datetime
from dateutil.rrule import rrule

date: datetime = None
t_stop: datetime = None

# event_model
header = ["doctor", "patient", date, t_stop, "dental_problema", "tooth_count", "fill_type"]

availibility_model = {
    "arzt": [
        rrule, 
        rrule
    ]
}
