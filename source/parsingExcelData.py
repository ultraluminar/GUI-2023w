from pandas import read_excel, DataFrame
from json import dump
from warnings import catch_warnings, filterwarnings
from dateutil.relativedelta import weekday

from classes.authentication_service import mhash


path_data = "source/data"
path_excel = "source/data/data.xlsx"
password_hashes = {}


class ExcelToCSV:
    def __init__(self, sheet: str, header: int, cols: str, csv_name: str):
        self.df = read_excel(io=path_excel, sheet_name=sheet, header=header, usecols=cols)
        self.csv_name = csv_name

    def __enter__(self):
        return self.df

    def __exit__(self, *args):
        self.df.to_csv(path_or_buf=f"{path_data}/{self.csv_name}.csv", index=False)


def parseKrankenKassenArt(inplace: bool) -> None:
    for index, row in df_doctors.iterrows():
        behandelt = row["behandelt"]

        for art in ["privat", "gesetzlich", "freiwillig gesetzlich"]:
            with catch_warnings():
                filterwarnings(action="ignore", category=FutureWarning)
                df_doctors.at[index, art] = art in behandelt

def parseBehandlungsZeiten() -> dict:
    kuerzel = ["Mo", "Di", "Mi", "Do", "Fr"]
    week = [str(weekday(x)) for x in range(5)]

    data_doctors = {}
    for _, row in df_doctors.iterrows():
        dic = {day: [] for day in week}
        zeiten_string = row["Behandlungszeiten"]

        for old in [":", " Uhr", " und"]:
            zeiten_string = zeiten_string.replace(old, '')

        for sub in zeiten_string.split():
            if sub[0].isalpha():
                start, stop = (kuerzel.index(sub.split('-')[idx]) for idx in (0, -1))
                days = week[start: stop + 1]
            else:
                hours = tuple(map(int, sub.split('-')))
                for day in days:
                    dic[day].append(hours)

        data_doctors[row["Zahnarzt"]] = dic
    return data_doctors

def parseDentaleProblematik(inplace: bool) -> None:
    for index, row in df_costs.loc[df_costs["Dentale Problematik"].notna()].iterrows():
        df_costs.loc[[index + 1, index + 2], "Dentale Problematik"] = row["Dentale Problematik"]

def parsePasswords(df) -> dict:
    return {row["Name"]: mhash(row["ID/Passwort"]) for _, row in df_doctors.iterrows()}

print("parsing doctors ...")
with ExcelToCSV(sheet="Zahnärzte", header=2, cols="B:E", csv_name="doctors") as df_doctors:
    parseKrankenKassenArt(inplace=True)
    behandlungszeiten = parseBehandlungsZeiten()
    df_doctors.rename(columns={"Zahnarzt": "Name"}, inplace=True)
    password_hashes |= parsePasswords(df_doctors)
    df_doctors = df_doctors[["Name", "ID/Passwort", "behandelt", "Behandlungszeiten", "privat", "gesetzlich", "freiwillig gesetzlich"]]

print("parsing patients ... ")
with ExcelToCSV(sheet="Stamm-Patienten", header=3, cols="C:G", csv_name="patiens") as df_patients:
    df_patients.rename(columns={"Patient": "Name"}, inplace=True)
    password_hashes |= parsePasswords(df_patients)
    df_patients = df_patients[["Name", "ID/Passwort", "Krankenkassenart", "Dentale Problematik", "Anzahl zu behandelnder Zähne"]]

print("parsing costs ...")
with ExcelToCSV(sheet="Kosten und Behandlungsdauer", header=3, cols="B:G", csv_name="costs") as df_costs:
    parseDentaleProblematik(inplace=True)
    df_costs.rename(columns={"Unnamed: 5": "gesetzlicher Anteil", "Unnamed: 6": "privater Anteil"}, inplace=True)

print("creating json files ...")
with open(f"{path_data}/pwd.json", mode="w", encoding="utf-8") as filestream:
    dump(password_hashes, filestream, indent=4, ensure_ascii=False)

with open("source/data/data_doctors.json", mode="w") as file:
    dump(behandlungszeiten, file, indent=4)