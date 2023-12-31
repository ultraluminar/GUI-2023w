from pandas import read_excel
from json import dump
from dateutil.rrule import rrule, WEEKLY
from warnings import catch_warnings

from auth_util import mhash

path_data = "data"
path_excel = "data/data.xlsx"
password_hashes = {}


class ExcelToCSV:
    """
    A class for converting Excel data to CSV format using context manager.

    Usage:
        with ExcelToCSV(sheet='Sheet1', header=0, cols='A:C', csv_name='data') as converter:
            # Perform operations on the converter object
    """

    def __init__(self, sheet: str, header: int, cols: str, csv_name: str):
        """
        Initializes the ExcelToCSV class.
        
        Args:
            sheet (str): The name of the sheet to be converted.
            header (int): The row number to be used as the header.
            cols (str): The columns to be converted.
            csv_name (str): The name of the CSV file to be created.
        """
        self.df = read_excel(io=path_excel, sheet_name=sheet, header=header, usecols=cols)
        self.csv_name = csv_name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.df.to_csv(path_or_buf=f"{path_data}/{self.csv_name}.csv", index=False)


def parseKrankenKassenArt(inplace: bool) -> None:
    """
    Parses the 'behandelt' column in the 'doctors.df' DataFrame and updates the 'privat', 'gesetzlich',
    and 'freiwillig gesetzlich' columns based on the values in 'behandelt'.
    """
    for index, row in doctors.df.iterrows():
        behandelt: str = row["behandelt"]

        with catch_warnings(category=FutureWarning, action="ignore"):
            for art in ["privat", "gesetzlich", "freiwillig gesetzlich"]:
                doctors.df.at[index, art] = art in behandelt


def parseBehandlungsZeiten() -> dict[str, list[str]]:
    """
    Parses the treatment times from the Excel data and returns a dictionary
    containing the treatment rules for each doctor.

    Returns:
        A dictionary where the keys are the names of the doctors and the values
        are lists of treatment rules.
    """
    kuerzel = ["Mo", "Di", "Mi", "Do", "Fr"]

    data_doctors = {}
    for _, row in doctors.df.iterrows():
        zeiten_string: str = row["Behandlungszeiten"]
        rules = []

        for old in [":", " Uhr", " und"]:
            zeiten_string = zeiten_string.replace(old, '')

        for sub in zeiten_string.split(' '):
            if sub[0].isalpha():
                start, stop = (kuerzel.index(sub.split('-')[idx]) for idx in (0, -1))
                days = range(start, stop + 1)
            else:
                start, stop = sub.split('-')
                hours = (int(start), int(stop))  # exclusive
                rule = rrule(freq=WEEKLY, byweekday=days, byhour=hours, byminute=0, bysecond=0)
                rules += [str(rule).split("\n")[1]]

        data_doctors[row["Zahnarzt"]] = rules
    return data_doctors


def parseDentaleProblematik(inplace: bool) -> None:
    """
    Parses the dental problems from the DataFrame and updates the values in the "Dentale Problematik" column.
    """
    for index, row in costs.df.loc[costs.df["Dentale Problematik"].notna()].iterrows():
        costs.df.loc[[index + 1, index + 2], "Dentale Problematik"] = row["Dentale Problematik"]


def parsePasswords(df) -> dict:
    """
    Parses the passwords from a DataFrame and returns a dictionary with the names as keys and hashed passwords as values.

    Args:
        df (pandas.DataFrame): The DataFrame containing the passwords.

    Returns:
        dict: A dictionary with the names as keys and hashed passwords as values.
    """
    return {row["Name"]: mhash(row["ID/Passwort"]) for _, row in df.iterrows()}


with ExcelToCSV(sheet="Zahnärzte", header=2, cols="B:E", csv_name="doctors") as doctors:
    parseKrankenKassenArt(inplace=True)
    behandlungszeiten = parseBehandlungsZeiten()
    doctors.df.rename(columns={"Zahnarzt": "Name"}, inplace=True)
    doctors.df["Username"] = doctors.df["Name"]
    password_hashes |= parsePasswords(doctors.df)
    doctors.df = doctors.df[["Username", "Name", "ID/Passwort", "privat", "gesetzlich", "freiwillig gesetzlich"]]

with ExcelToCSV(sheet="Stamm-Patienten", header=3, cols="C:G", csv_name="patients") as patients:
    patients.df.rename(columns={"Patient": "Name"}, inplace=True)
    patients.df["Username"] = patients.df["Name"]
    password_hashes |= parsePasswords(patients.df)
    patients.df = patients.df[["Username", "Name", "ID/Passwort", "Krankenkassenart", "Dentale Problematik",
                               "Anzahl zu behandelnder Zähne"]]

with ExcelToCSV(sheet="Kosten und Behandlungsdauer", header=3, cols="B:G", csv_name="costs") as costs:
    parseDentaleProblematik(inplace=True)
    costs.df.rename(columns={"Unnamed: 5": "gesetzlicher Anteil", "Unnamed: 6": "privater Anteil"}, inplace=True)

with open(f"{path_data}/pwd.json", mode="w", encoding="utf-8") as file:
    dump(password_hashes, file, indent=4, ensure_ascii=False)

with open(f"{path_data}/doctors_free.json", mode="w", encoding="utf-8") as file:
    dump(behandlungszeiten, file, indent=4)

# create new csv file for appointments with header ["doctor", "patient", date, t_stop, "dental_problem", "tooth_count", "fill_type"]
with open(f"{path_data}/appointments.csv", mode="w", encoding="utf-8") as file:
    file.write("Doctor,Patient,dt_start,dt_stop,dental_problem,tooth_count,fill_type\n")