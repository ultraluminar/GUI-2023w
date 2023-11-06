import pandas as pd

from random import randint
from bcrypt import hashpw, checkpw, gensalt
from csv import writer
from json import load, dump

# variables
patients_file_path = "source/data/patients.csv"
password_file_path = "source/data/pwd.json"
    

def check_login(username: str, password: str) -> bool:
    passwords: dict = load_passwords()
    return mcheck(password, passwords[username])

def add_patient(patient_data: list):
    passwords: dict = load_passwords()
    
    passwords[patient_data[0]] = mhash(patient_data[1])
    with open(password_file_path, mode="w") as filestream:
        dump(passwords, filestream, indent=4)
    
    patient_data[1] = generate_unique_patient_id()
    with open(patients_file_path, mode='a', newline='') as file:
        writing = writer(file)
        writing.writerow(patient_data)

def username_exists(username: str) -> bool:
    passwords: dict = load_passwords()
    return username in passwords.keys()

def mhash(plain: str) -> str:
    return hashpw(plain.encode(), gensalt()).decode()

def mcheck(user: str, pwd: str) -> bool:
    return checkpw(user.encode(), pwd.encode())
            
def generate_unique_patient_id() -> str:
    existing_ids = set()
    
    # Load the existing IDs from the CSV file
    try:
        df = pd.read_csv(patients_file_path)
        existing_ids = set(df["ID/Passwort"])
    except FileNotFoundError:
        # Handle the case when the file doesn't exist
        pass
    
    while True:
        new_id = f"P{randint(100, 999)}"
        if new_id not in existing_ids:
            return new_id
        
def load_passwords():
    # loading password.json in as dict
    with open(password_file_path, mode="r") as filestream:
        return load(filestream)