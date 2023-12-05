from typing import Literal

from pandas import read_csv
from random import randint
from bcrypt import hashpw, checkpw, gensalt
from csv import writer
from json import load, dump

# variables
patients_file_path = "data/patients.csv"
doctors_file_path = "data/doctors.csv"
password_file_path = "data/pwd.json"
data_doctors_path = "data/data_doctors.json"


def mhash(plain: str) -> str:
    # wenig rounds da wir nicht wirklich security brauchen
    return hashpw(plain.encode(), gensalt(rounds=8)).decode()


def mcheck(user: str, pwd: str) -> bool:
    return checkpw(user.encode(), pwd.encode())


def appendCSV(path: str, row: iter):
    with open(path, mode='a', newline='', encoding="utf-8") as file:
        writer(file).writerow(row)

def loadJson(path: str) -> dict:
    with open(path, mode='r', encoding="utf-8") as file:
        return load(file)

def updateJson(path: str, dic: dict):
    old = loadJson(path)

    if any(key in old for key in dic.keys()):
        raise ValueError("at least on key already in dict!")

    with open(path, mode="w", encoding="utf-8") as file:
        dump(old | dic, file, indent=4, ensure_ascii=False)

def gen_UID(path: str, prefix: str) -> str:
    ids = list(read_csv(path)["ID/Passwort"])
    while True:
        new_id = f"{prefix}{randint(100, 999)}"
        if new_id not in ids:
            return new_id


def username_exists(username: str) -> bool:
    return username in loadJson(password_file_path).keys()



class AuthenticationService:
    def __init__(self):
        self.username = None


    def check_login(self, username: str, password: str) -> bool:
        if mcheck(password, loadJson(password_file_path)[username]):
            self.username = username
            return True
        return False


    def add_doctor(self, doctor_data: dict):
        updateJson(password_file_path, {doctor_data["username"]: mhash(doctor_data["password"])})
        updateJson(data_doctors_path, {doctor_data["username"]: doctor_data["availability"]})

        doctor_data["password"] = gen_UID(doctors_file_path, 'A')
        doctor_data.pop("availability")
        appendCSV(doctors_file_path, doctor_data.values())


    def add_patient(self, patient_data: dict):
        updateJson(password_file_path, {patient_data["username"]: mhash(patient_data["password"])})

        patient_data["password"] = gen_UID(patients_file_path, 'P')
        appendCSV(patients_file_path, patient_data.values())