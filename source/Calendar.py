from pandas import read_csv
from json import load, dump, dumps
from dateutil.relativedelta import weekday


# getting data from doctors.csv
df_doctors = read_csv("source/data/doctors.csv")
df_patients = read_csv("source/data/patients.csv")

kuerzel = ["Mo", "Di", "Mi", "Do", "Fr"]
tage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
week = [weekday(x) for x in range(5)]
zeiten = range(8, 18+1)

def parse_days(sub: str) -> list[weekday]:
    if '-' not in sub:
        return [week[kuerzel.index(sub)]]
    start, stop = [kuerzel.index(subsub) for subsub in sub.split('-')]
    return week[start: stop+1]

def setZeiten(string: str, doc: str):
    current_days, hour_tuple = [], []
    for sub in string.split(' '):
        if sub[0].isalpha():  # wenn sub Tage darstellt
            current_days = parse_days(sub)

        elif sub[0].isdigit():  # wenn sub Stunden darstellt
            hour_tuple = sub.split('-')

            for day in current_days:
                    data_doctors[doc][str(day)] += [hour_tuple]

data_doctors = {arzt: {str(day): [] for day in week} for arzt in df_doctors["Zahnarzt"]}

for index, row in df_doctors.iterrows():
    setZeiten(row["Behandlungszeiten"], row["Zahnarzt"])



with open("source/data/data_doctors.json", mode="w") as file:
    dump(data_doctors, file, indent=4)

data_patients = {patient: [] for patient in df_patients["Patient"]}

