from pandas import read_excel
from json import dump
from classes.authentication_service import mhash

from warnings import catch_warnings, filterwarnings

def behandelt_analyse(df):
    week = ["Mo", "Di", "Mi", "Do", "Fr"]

    for index, row in df.iterrows():
        behandelt = row["behandelt"].lstrip("nur ").split(" und ")

        for art in ["privat", "gesetzlich", "freiwillig gesetzlich"]:
            with catch_warnings():
                filterwarnings(action="ignore", category=FutureWarning)
                df.at[index, art] = art in behandelt


        text = row["Behandlungszeiten"].replace(":", '').replace(" Uhr", '').replace(" und", '')
        df.at[index, "Behandlungszeiten"] = text
    return df

file_path = "source/data/data.xlsx"
new_file_directory_path = "source/data"

# parsing the inital data excel file to csv files

# parsing the doctors table
print("parsing doctors...")
df_doctors = read_excel(io=file_path, sheet_name="Zahnärzte", header=2, usecols="B:E")
df_doctors = behandelt_analyse(df_doctors)
df_doctors["Name"] = df_doctors["Zahnarzt"]
df_doctors = df_doctors[["Zahnarzt", "Name", "ID/Passwort", "behandelt", "Behandlungszeiten", "privat", "gesetzlich", "freiwillig gesetzlich"]]
df_doctors.to_csv(path_or_buf=f"{new_file_directory_path}/doctors.csv", index=False)
print("success")

# parsing the patients table
print("parsing patients...")
df_patients = read_excel(io=file_path, sheet_name="Stamm-Patienten", header=3, usecols="C:G")
df_patients["Name"] = df_patients["Patient"]
df_patients = df_patients[["Patient", "Name", "ID/Passwort", "Krankenkassenart", "Dentale Problematik", "Anzahl zu behandelnder Zähne"]]
df_patients.to_csv(path_or_buf=f"{new_file_directory_path}/patients.csv", index=False)
print("success")

# hashing passwords
print("hashing initial passwords...")
df_patients["Hash"] = df_patients["ID/Passwort"].map(mhash)
df_doctors["Hash"] = df_doctors["ID/Passwort"].map(mhash)
df_doctors = df_doctors.rename(columns={'Zahnarzt': 'Patient'})
df_passwords = df_patients[["Patient", "Hash"]]
# TODO This already works but you get one warning somehow:
for index, row in df_doctors.iterrows():
    index = len(df_passwords)
    df_passwords.loc[index, "Patient"] = row["Patient"]
    df_passwords.loc[index, "Hash"] = row["Hash"]
password_dict = df_passwords.to_dict(orient="records")
json_data = {item["Patient"]: item["Hash"] for item in password_dict}
print("creating json file...")
with open(f"{new_file_directory_path}/pwd.json", "w", encoding="utf-8") as filestream:
    dump(json_data, filestream, indent=4, ensure_ascii=False)
print("success")

# parsing the costs table
print("parsing costs...")
df_costs = read_excel(io=file_path, sheet_name="Kosten und Behandlungsdauer", header=3, usecols="B:G")
# replacing column names that are missing in the excel file
print("replacing missing fields...")
df_costs.rename(columns={"Unnamed: 5": "gesetzlicher Anteil", "Unnamed: 6": "privater Anteil"}, inplace=True)

# adding the "Dentale Problematik" column in every row instead of only the first
print("adding missing dental problem column...")
dental_problem = ""

for index, row in df_costs.loc[df_costs["Dentale Problematik"].notna()].iterrows():
    df_costs.loc[[index+1, index+2], "Dentale Problematik"] = row["Dentale Problematik"]


df_costs.to_csv(path_or_buf=f"{new_file_directory_path}/costs.csv", index=False)
print("success")
