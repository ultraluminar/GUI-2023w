from pandas import read_csv
from json import load, dump, dumps

# getting data from doctors.csv
df_doctors = read_csv("source/data/doctors.csv")
df_patients = read_csv("source/data/patients.csv")


wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
behandlungszeiten = range(8, 18+1)


data_doctors = {arzt: {"all": [], "busy": []} for arzt in df_doctors["Zahnarzt"]}
data_patients = {patient: [] for patient in df_patients["Patient"]}

print(dumps(data_doctors, indent=4))
print(dumps(data_patients, indent=4))
