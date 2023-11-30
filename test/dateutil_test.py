from dateutil.relativedelta import weekday
from collections import ChainMap

week_str = ["Mo", "Di", "Mi", "Do", "Fr"]
week_obj = [weekday(x) for x in range(5)]

tuptup = [(("Mo", "Fr"), (8, 12)),
          (("Mo", "Fr"), (14, 16)),
          (("Di", "Mi"), (16, 18))]

ranges = []
for day_tuple, time_tuple in tuptup:
    start, stop = [week_str.index(x) for x in day_tuple]
    ranges.append({weekday(x): time_tuple for x in range(start, stop+1)})


ranges_combined = {key: [dic[key] for dic in ranges if key in dic] for key in week_obj}
print(ranges_combined)