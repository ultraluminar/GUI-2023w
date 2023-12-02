from pandas import read_excel, DataFrame
from json import dump
from warnings import catch_warnings, filterwarnings

from classes.authentication_service import mhash


path_data = "source/data"
path_excel = "source/data/data.xlsx"
data_pwd = {}


class ExcelToCSV:
    def __init__(self, sheet: str, header: int, cols: str, csv_name: str):
        self.df = read_excel(io=path_excel, sheet_name=sheet, header=header, usecols=cols)
        self.csv_name = csv_name

    def __enter__(self):
        return self.df

    def __exit__(self, *args):
        self.df.to_csv(path_or_buf=f"{path_data}/{self.csv_name}.csv", index=False)


print("parsing doctors ...")
with ExcelToCSV(sheet="Zahnärzte", header=2, cols="B:E", csv_name="doctors") as df_doctors:
    for index, row in df_doctors.iterrows():
        behandelt = row["behandelt"].lstrip("nur ").split(" und ")

        for art in ["privat", "gesetzlich", "freiwillig gesetzlich"]:
            with catch_warnings():
                filterwarnings(action="ignore", category=FutureWarning)
                df_doctors.at[index, art] = art in behandelt
    df_doctors.rename(columns={"Zahnarzt": "Name"}, inplace=True)
    data_pwd.update({row["Name"]: mhash(row["ID/Passwort"]) for _, row in df_doctors.iterrows()})
    df_doctors = df_doctors[["Name", "ID/Passwort", "behandelt", "Behandlungszeiten", "privat", "gesetzlich", "freiwillig gesetzlich"]]

print("parsing patients ... ")
with ExcelToCSV(sheet="Stamm-Patienten", header=3, cols="C:G", csv_name="patiens") as df_patients:
    df_patients.rename(columns={"Patient": "Name"}, inplace=True)
    data_pwd.update({row["Name"]: mhash(row["ID/Passwort"]) for _, row in df_patients.iterrows()})
    df_patients = df_patients[["Name", "ID/Passwort", "Krankenkassenart", "Dentale Problematik", "Anzahl zu behandelnder Zähne"]]

print("creating json file ...")
with open(f"{path_data}/pwd.json", mode="w", encoding="utf-8") as filestream:
    dump(data_pwd, filestream, indent=4, ensure_ascii=False)

print("parsing costs ...")
with ExcelToCSV(sheet="Kosten und Behandlungsdauer", header=3, cols="B:G", csv_name="costs") as df_costs:
    df_costs.rename(columns={"Unnamed: 5": "gesetzlicher Anteil", "Unnamed: 6": "privater Anteil"}, inplace=True)  # replacing column names that are missing in the excel file
    for index, row in df_costs.loc[df_costs["Dentale Problematik"].notna()].iterrows():
        df_costs.loc[[index + 1, index + 2], "Dentale Problematik"] = row["Dentale Problematik"]  # adding the "Dentale Problematik" column in every row instead of only the first
