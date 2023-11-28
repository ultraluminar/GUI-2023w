from pandas import read_csv
from json import load, dump, dumps

# getting data from doctors.csv
df_doctors = read_csv("source/data/doctors.csv")
df_patients = read_csv("source/data/patients.csv")

kuerzel = ["Mo", "Di", "Mi", "Do", "Fr"]
tage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
zeiten = range(8, 18+1)
def setZeiten(string: str, doc: str):
    lis, current_days = [], []
    for sub in string.split(' '):
        if sub[0].isalpha():
            if '-' in sub:
                first, last = [kuerzel.index(subsub) for subsub in sub.split('-')]
                current_days = tage[first: last+1]
            else:
                current_days = [tage[kuerzel.index(sub)]]
        elif sub[0].isdigit():
            first, last = sub.split('-')
            current_zeiten = range(int(first), int(last)) if '-' in sub else sub
            for day in current_days:
                for hour in current_zeiten:
                    data_doctors[doc][day][hour]["busy"] = False


termin = {"Tag": "Dienstag", "Zeit": 9}

data_doctors = {arzt: {day: {hour: {} for hour in zeiten} for day in tage} for arzt in df_doctors["Zahnarzt"]}
for index, row in df_doctors.iterrows():
    setZeiten(row["Behandlungszeiten"], row["Zahnarzt"])

with open("source/data/data_doctors.json", mode="x") as file:
    dump(data_doctors, file, indent=4)

data_patients = {patient: [] for patient in df_patients["Patient"]}

