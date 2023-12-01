from pandas import read_csv, Series
from json import load, dump, dumps
from dateutil.relativedelta import weekday


# getting data from doctors.csv
df_doctors = read_csv("source/data/doctors.csv")
# df_patients = read_csv("source/data/patients.csv")

kuerzel = ["Mo", "Di", "Mi", "Do", "Fr"]
week = [weekday(x) for x in range(5)]
zeiten = range(8, 18 + 1)


def getZeiten(zeiten_string: str) -> dict:
    days, hours = [], []
    dic = {str(day): [] for day in week}
    for sub in zeiten_string.split(' '):
        if sub[0].isalpha():
            if '-' not in sub:  # kein bindestrich
                days = [week[kuerzel.index(sub)]]
            else:
                start, stop = (kuerzel.index(subsub) for subsub in sub.split('-'))
                days = week[start: stop+1]
        elif sub[0].isdigit():
            for day in days:
                dic[str(day)].append(tuple(sub.split('-')))
    return dic


data_doctors = {row["Zahnarzt"]: getZeiten(row["Behandlungszeiten"]) for index, row in df_doctors.iterrows()}

with open("source/data/data_doctors.json", mode="w") as file:
    dump(data_doctors, file, indent=4)

# data_patients = {patient: [] for patient in df_patients["Patient"]}
