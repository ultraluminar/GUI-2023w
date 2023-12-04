from pandas import read_excel
from json import dump
from dateutil.rrule import rrule, WEEKLY
from warnings import catch_warnings

from classes.authentication_service import mhash


path_data = "data"
path_excel = "data/data.xlsx"
password_hashes = {}


class ExcelToCSV:
    def __init__(self, sheet: str, header: int, cols: str, csv_name: str):
        self.df = read_excel(io=path_excel, sheet_name=sheet, header=header, usecols=cols)
        self.csv_name = csv_name

    def __enter__(self):
        return self.df

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.df.to_csv(path_or_buf=f"{path_data}/{self.csv_name}.csv", index=False)


def parseKrankenKassenArt(inplace: bool) -> None:
    for index, row in df_doctors.iterrows():
        behandelt: str = row["behandelt"]

        with catch_warnings(category=FutureWarning, action="ignore"):
            for art in ["privat", "gesetzlich", "freiwillig gesetzlich"]:
                df_doctors.at[index, art] = art in behandelt

def parseBehandlungsZeiten() -> dict[str, list[str]]:
    kuerzel = ["Mo", "Di", "Mi", "Do", "Fr"]

    data_doctors = {}
    for _, row in df_doctors.iterrows():
        zeiten_string: str = row["Behandlungszeiten"]
        rules = []

        for old in [":", " Uhr", " und"]:
            zeiten_string = zeiten_string.replace(old, '')

        for sub in zeiten_string.split(' '):
            if sub[0].isalpha():
                start, stop = (kuerzel.index(sub.split('-')[idx]) for idx in (0, -1))
                days = range(start, stop+1)
            else:
                start, stop = sub.split('-')
                hours = range(int(start), int(stop))  # exclusive
                rule = rrule(freq=WEEKLY, byweekday=days, byhour=hours, byminute=0, bysecond=0)
                rules += [str(rule).split("\n")[1]]


        data_doctors[row["Zahnarzt"]] = rules
    return data_doctors


def parseDentaleProblematik(inplace: bool) -> None:
    for index, row in df_costs.loc[df_costs["Dentale Problematik"].notna()].iterrows():
        df_costs.loc[[index + 1, index + 2], "Dentale Problematik"] = row["Dentale Problematik"]

def parsePasswords(df) -> dict:
    return {row["Name"]: mhash(row["ID/Passwort"]) for _, row in df.iterrows()}


with ExcelToCSV(sheet="Zahnärzte", header=2, cols="B:E", csv_name="doctors") as df_doctors:
    parseKrankenKassenArt(inplace=True)
    behandlungszeiten = parseBehandlungsZeiten()
    df_doctors.rename(columns={"Zahnarzt": "Name"}, inplace=True)
    df_doctors["Username"] = df_doctors["Name"]
    password_hashes |= parsePasswords(df_doctors)
    df_doctors = df_doctors[["Username", "Name", "ID/Passwort", "behandelt", "Behandlungszeiten", "privat", "gesetzlich", "freiwillig gesetzlich"]]

with ExcelToCSV(sheet="Stamm-Patienten", header=3, cols="C:G", csv_name="patiens") as df_patients:
    df_patients.rename(columns={"Patient": "Name"}, inplace=True)
    df_doctors["Username"] = df_doctors["Name"]
    password_hashes |= parsePasswords(df_patients)
    df_patients = df_patients[["Username", "Name", "ID/Passwort", "Krankenkassenart", "Dentale Problematik", "Anzahl zu behandelnder Zähne"]]

with ExcelToCSV(sheet="Kosten und Behandlungsdauer", header=3, cols="B:G", csv_name="costs") as df_costs:
    parseDentaleProblematik(inplace=True)
    df_costs.rename(columns={"Unnamed: 5": "gesetzlicher Anteil", "Unnamed: 6": "privater Anteil"}, inplace=True)

with open(f"{path_data}/pwd.json", mode="w", encoding="utf-8") as file:
    dump(password_hashes, file, indent=4, ensure_ascii=False)

with open(f"{path_data}/data_doctors.json", mode="w", encoding="utf-8") as file:
    dump(behandlungszeiten, file, indent=4)