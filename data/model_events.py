from typing import Literal
from datetime import time, datetime
from dateutil.rrule import rrule

event_model = {
    "arzt": {
        "patient": {
            datetime: {
                "t_stop": datetime,   # 8 bis 18 Uhr
                "dental_problem": Literal["Karies klein", "Karies groß", "Teilkrone", "Krone", "Wurzelbehandlung"],
                "tooth_count": int,
                "fill_type": Literal["normal", "höherwertig", "höchstwertig"]
            }
        }
    }
}

availibility_model = {
    "arzt": [
        rrule, 
        rrule
    ]
}
