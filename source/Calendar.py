from pandas import read_csv
from json import dump
from dateutil.relativedelta import weekday


df_doctors = read_csv("source/data/doctors.csv")

kuerzel = ["Mo", "Di", "Mi", "Do", "Fr"]
week = [str(weekday(x)) for x in range(5)]

def getZeiten(zeiten_string: str) -> dict:
    dic = {day: [] for day in week}

    for sub in zeiten_string.split():
        if sub[0].isalpha():
            start, stop = (kuerzel.index(sub.split('-')[idx]) for idx in (0, -1))
            days = week[start: stop+1]

        elif sub[0].isdigit():
            hours = tuple(map(int, sub.split('-')))
            for day in days:
                dic[day].append(hours)

    return dic


data_doctors = {row["Zahnarzt"]: getZeiten(row["Behandlungszeiten"]) for index, row in df_doctors.iterrows()}
print(data_doctors)

with open("source/data/data_doctors.json", mode="w") as file:
    dump(data_doctors, file, indent=4)
