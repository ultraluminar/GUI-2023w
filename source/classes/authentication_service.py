import pandas as pd

from random import randint
from bcrypt import hashpw, checkpw, gensalt
from csv import writer
from json import load, dump

# variables
patients_file_path = "source/data/patients.csv"
password_file_path = "source/data/pwd.json"


def mhash(plain: str) -> str:
    return hashpw(plain.encode(), gensalt()).decode()


def mcheck(user: str, pwd: str) -> bool:
    return checkpw(user.encode(), pwd.encode())


def load_passwords():
    # loading password.json in as dict
    with open(password_file_path, mode="r", encoding="utf-8") as filestream:
        return load(filestream)

class AuthenticationService:
    def __init__(self):
        self.username = None


    def check_login(self, username: str, password: str) -> bool:
        passwords: dict = load_passwords()
        if not password:
            return False
        if mcheck(password, passwords[username]):
            self.username = username
            return True
        return False


    def add_patient(self, patient_data: dict):
        passwords: dict = load_passwords()

        passwords[patient_data["username"]] = mhash(patient_data["password"])
        with open(password_file_path, mode="w", encoding="utf-8") as filestream:
            dump(passwords, filestream, indent=4, ensure_ascii=False)

        patient_data["password"] = self.generate_unique_patient_id()
        with open(patients_file_path, mode='a', newline='', encoding="utf-8") as file:
            writing = writer(file)
            writing.writerow(patient_data.values())

    def update_password(self, new_password: str):
        passwords: dict = load_passwords()
        passwords[self.username] = mhash(new_password)

        with open(password_file_path, mode="w", encoding="utf-8") as filestream:
            dump(passwords, filestream, indent=4, ensure_ascii=False)

    @staticmethod
    def generate_unique_patient_id() -> str:
        existing_ids = set()

        # Load the existing IDs from the CSV file
        df = pd.read_csv(patients_file_path)
        existing_ids = set(df["ID/Passwort"])

        while True:
            new_id = f"P{randint(100, 999)}"
            if new_id not in existing_ids:
                return new_id

    @staticmethod
    def username_exists(username: str) -> bool:
        passwords: dict = load_passwords()
        return username in passwords.keys()

