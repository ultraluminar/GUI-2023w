from pathlib import Path
from pandas import read_csv
from random import randint, choices
from bcrypt import hashpw, checkpw, gensalt
from csv import writer
from json import load, dump

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# variables
paths = {
    "passwords": Path("data/pwd.json"),
    "appointments": Path("data/appointments.csv"),
    "patients": {"csv": Path("data/patients.csv")},
    "doctors": {"csv": Path("data/doctors.csv"),
                "free": Path("data/doctors_free.json")}
}

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"


def random_chars(n: int) -> str:
    return "".join(choices(population=alphabet, k=n))

def mhash(plain: str) -> str:
    # wenig rounds da wir nicht wirklich security brauchen
    return hashpw(plain.encode(), gensalt(rounds=8)).decode()


def mcheck(user: str, pwd: str) -> bool:
    return checkpw(user.encode(), pwd.encode())


def appendCSV(path: Path, row: iter):
    with open(path, mode='a', newline='', encoding="utf-8") as file:
        writer(file).writerow(row)

def getfromCSV(path: Path, filter: tuple[str, str], field: str = None):
    df = read_csv(path)

    df.set_index(filter[0], inplace=True)
    df = df.loc[filter[1]]

    return df if field is None else df[field]

def updateCSV(path: Path, filter: tuple[str, str], update: tuple[str, str]):
    df = read_csv(path)

    df.set_index(filter[0], inplace=True)
    df.loc[filter[1], update[0]] = update[1]
    df.reset_index(inplace=True)
    df.to_csv(path, index=False)


def loadJson(path: Path) -> dict:
    with open(path, mode='r', encoding="utf-8") as file:
        return load(file)

def updateJson(path: Path, dic: dict, replace=False):
    old = loadJson(path)

    print(dic.keys(), old.keys(), "update JSON")
    if replace and any(key not in old for key in dic.keys()):
        raise ValueError("key not in dict!")
    elif not replace and any(key in old for key in dic.keys()):
        raise ValueError("key already in dict!")

    with open(path, mode="w", encoding="utf-8") as file:
        dump(old | dic, file, indent=4, ensure_ascii=False)

def gen_UID(path: Path, prefix: str) -> str:
    ids = list(read_csv(path)["ID/Passwort"])
    while True:
        new_id = f"{prefix}{randint(100, 999)}"
        if new_id not in ids:
            return new_id


def add_doctor(doctor_data: dict):
    updateJson(paths["passwords"], {doctor_data["username"]: mhash(doctor_data["password"])})
    updateJson(paths["doctors"]["free"], {doctor_data["username"]: doctor_data["availability"]})
    print("free")

    doctor_data["password"] = gen_UID(paths["doctors"]["csv"], 'A')
    doctor_data.pop("availability")
    appendCSV(paths["doctors"]["csv"], doctor_data.values())


def add_patient(patient_data: dict):
    updateJson(paths["passwords"], {patient_data["username"]: mhash(patient_data["password"])})

    patient_data["password"] = gen_UID(paths["patients"]["csv"], 'P')
    appendCSV(paths["patients"]["csv"], patient_data.values())


def username_exists(username: str) -> bool:
    return username in loadJson(paths["passwords"]).keys()


class AuthenticationService:
    def __init__(self):
        self.username = None
        self.code = None

    def update_password(self, new_password: str):
        updateJson(paths["passwords"], {self.username: mhash(new_password)}, replace=True)

    def check_login(self, username: str, password: str) -> bool:
        if not username_exists(username):
            return False
        elif not mcheck(password, loadJson(paths["passwords"])[username]):
            return False
        else:
            self.username = username
            return True

    def generate_code(self):
        if self.code is None:
            self.code = random_chars(8)

    def check_code(self, code: str):
        return code == self.code