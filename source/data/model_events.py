from typing import Literal
from datetime import time, date, timedelta
from dateutil.relativedelta import weekday

event_model = {
    "arzt": {
        "patient": {
            date: {
                "start_time": time, # 8 bis 18 Uhr
                "end_time": time,   # 8 bis 18 Uhr
                "dental_problem": Literal["Karies klein", "Karies groß", "Teilkrone", "Krone", "Wurzelbehandlung"],
                "tooth_count": int,
                "fill_type": Literal["normal", "höherwertig", "höchstwertig"]
            }
        }
    }
}

availibility_model = {
    "arzt": {
        weekday: {
            "deltas": [timedelta, timedelta]
        }
    }
}
