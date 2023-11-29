from pandas import read_csv
from json import load, dump, dumps

# getting data from doctors.csv
df_doctors = read_csv("source/data/doctors.csv")
df_patients = read_csv("source/data/patients.csv")

kuerzel = ["Mo", "Di", "Mi", "Do", "Fr"]
tage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
zeiten = range(8, 18+1)

def parse_days(sub: str) -> list[str]:
    if '-' not in sub:
        return [tage[kuerzel.index(sub)]]
    start, stop = [kuerzel.index(subsub) for subsub in sub.split('-')]
    return tage[start: stop+1]

def parse_hours(sub: str) -> list[int]:
    start, stop = sub.split('-')
    return list(range(int(start), int(stop)))

def setZeiten(string: str, doc: str):
    current_days, current_hour = [], []
    for sub in string.split(' '):
        if sub[0].isalpha():  # wenn sub Tage darstellt
            current_days = parse_days(sub)

        elif sub[0].isdigit():  # wenn sub Stunden darstellt
            current_hour = parse_hours(sub)

            for day in current_days:
                for hour in current_hour:
                    data_doctors[doc][day][hour]["busy"] = False


data_doctors = {arzt: {day: {hour: {} for hour in zeiten} for day in tage} for arzt in df_doctors["Zahnarzt"]}

for index, row in df_doctors.iterrows():
    setZeiten(row["Behandlungszeiten"], row["Zahnarzt"])

for doc, week in data_doctors.items():
    for day, hours in week.items():
        for hour, event in hours.items():
            if not event:
                print(f"{doc} hat {day}s um {hour} Uhr frei !")


with open("source/data/data_doctors.json", mode="w") as file:
    dump(data_doctors, file, indent=4)

data_patients = {patient: [] for patient in df_patients["Patient"]}

