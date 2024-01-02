from dateutil.rrule import rrule

# event_model
header = ["doctor", "patient", "dt_start", "dt_stop", "dental_problem", "tooth_count", "fill_type"]

availibility_model = {
    "arzt": [
        rrule, 
        rrule
    ]
}
