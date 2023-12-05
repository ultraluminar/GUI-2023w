from typing import Literal

from pandas import read_csv
from random import randint
from bcrypt import hashpw, checkpw, gensalt
from csv import writer, reader
from json import load, dump

# variables
patients_file_path = "data/patients.csv"
doctors_file_path = "data/doctors.csv"
password_file_path = "data/pwd.json"
data_doctors_path = "data/data_doctors.json"


def mhash(plain: str) -> str:
    return hashpw(plain.encode(), gensalt(rounds=8)).decode()  # wenig rounds da wir nicht wirklich security brachen


def mcheck(user: str, pwd: str) -> bool:
    return checkpw(user.encode(), pwd.encode())


class JsonFile(dict):
    def __init__(self, path: str, mode: Literal["r", "w"]):
        with open(path, mode="r", encoding="utf-8") as file:
            super().__init__(load(file))
        self.mode = mode
        self.path = path

    def __enter__(self) -> dict:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None and self.mode == "w":
            with open(self.path, mode="w", encoding="utf-8") as file:
                dump(self, file, indent=4, ensure_ascii=False)




def appendCSV(path: str, row: iter):
    with open(path, mode='a', newline='', encoding="utf-8") as file:
        writer(file).writerow(row)



class AuthenticationService:
    def __init__(self):
        self.username = None


    def check_login(self, username: str, password: str) -> bool:
        with JsonFile(password_file_path, mode='r') as file:
            if mcheck(password, file[username]):
                self.username = username
                return True
            return False


    def add_doctor(self, doctor_data: dict):
        with JsonFile(password_file_path, mode='w') as file_passwords:
            file_passwords[doctor_data["username"]] = mhash(doctor_data["password"])

        with JsonFile(data_doctors_path, mode='w') as file_data_doctors:
            file_data_doctors[doctor_data["username"]] = doctor_data["availability"]

        doctor_data["password"] = self.gen_UID(doctors_file_path)
        doctor_data.pop("availability")
        appendCSV(doctors_file_path, doctor_data.values())


    def add_patient(self, patient_data: dict):
        with JsonFile(password_file_path, mode='w') as file_passwors:
            file_passwors[patient_data["username"]] = mhash(patient_data["password"])

        patient_data["password"] = self.gen_UID(patients_file_path)
        appendCSV(patients_file_path, patient_data.values())


    @staticmethod
    def gen_UID(path: str) -> str:
        ids = list(read_csv(path)["ID/Passwort"])
        prefix = ids[0][0]
        while True:
            new_id = f"{prefix}{randint(100, 999)}"
            if new_id not in ids:
                return new_id

    @staticmethod
    def username_exists(username: str) -> bool:
        with JsonFile(password_file_path, mode='r') as file:
            return username in file.keys()

