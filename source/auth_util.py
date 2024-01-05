from pathlib import Path
from pandas import read_csv
from random import randint, choices
from bcrypt import hashpw, checkpw, gensalt
from csv import writer
from json import load, dump
import pandas

# variables
paths = {
    "passwords": Path("data/pwd.json"),
    "appointments": Path("data/appointments.csv"),
    "patients": {"csv": Path("data/patients.csv")},
    "doctors": {"csv": Path("data/doctors.csv"),
                "free": Path("data/doctors_free.json")}
}


def mhash(plain: str) -> str:
    """
    Hashes the given plain text password using bcrypt algorithm.

    Args:
        plain (str): The plain text password to be hashed.

    Returns:
        str: The hashed password.

    """
    return hashpw(plain.encode(), gensalt(rounds=8)).decode()


def mcheck(user: str, pwd: str) -> bool:
    """
    Check if the provided username and password match.

    Args:
        user (str): The username to check.
        pwd (str): The password to check.

    Returns:
        bool: True if the username and password match, False otherwise.
    """
    return checkpw(user.encode(), pwd.encode())



def appendCSV(path: Path, row: iter):
    """
    Append a row to a CSV file.

    Args:
        path (Path): The path to the CSV file.
        row (iter): The row to be appended to the CSV file.
    """
    with open(path, mode='a', newline='', encoding="utf-8") as file:
        writer(file).writerow(row)


def getfromCSV(path: Path, filter_tuple: tuple[str, str], field: str = None) -> pandas.Series | int:
    """
    Retrieves data from a CSV file based on a filter and optional field.

    Args:
        path (Path): The path to the CSV file.
        filter_tuple (tuple[str, str]): A tuple containing the filter column name and value.
        field (str, optional): The name of the field to retrieve. If not provided, returns the entire row.

    Returns:
        DataFrame: The filtered data from the CSV file.
    """
    df = read_csv(path)
    df.set_index(filter_tuple[0], inplace=True)
    df = df.loc[filter_tuple[1]]
    return df if field is None else df[field]


def updateCSV(path: Path, filter_tuple: tuple[str, str], update: tuple[str, str]):
    """
    Update a CSV file with new values based on a filter.

    Args:
        path (Path): The path to the CSV file.
        filter_tuple (tuple[str, str]): A tuple containing the column name and the filter value.
        update (tuple[str, str]): A tuple containing the column name and the new value.
    """
    df = read_csv(path)
    df.set_index(filter_tuple[0], inplace=True)
    df.loc[filter_tuple[1], update[0]] = update[1]
    df.reset_index(inplace=True)
    df.to_csv(path, index=False)


def loadJson(path: Path) -> dict:
    """
    Load a JSON file and return its contents as a dictionary.

    Args:
        path (Path): The path to the JSON file.

    Returns:
        dict: The contents of the JSON file as a dictionary.
    """
    with open(path, mode='r', encoding="utf-8") as file:
        return load(file)


def updateJson(path: Path, dic: dict, replace=False):
    """
    Update a JSON file with a dictionary.

    Args:
        path (Path): The path to the JSON file.
        dic (dict): The dictionary to update the JSON file with.
        replace (bool, optional): Whether to replace existing keys in the JSON file. Defaults to False.

    Raises:
        ValueError: If `replace` is True and a key in `dic` is not present in the JSON file.
        ValueError: If `replace` is False and a key in `dic` is already present in the JSON file.
    """
    old = loadJson(path)
    if replace and any(key not in old for key in dic.keys()):
        raise ValueError("key not in dict!")
    elif not replace and any(key in old for key in dic.keys()):
        raise ValueError("key already in dict!")
    with open(path, mode="w", encoding="utf-8") as file:
        dump(old | dic, file, indent=4, ensure_ascii=False)


def gen_UID(path: Path, prefix: str) -> str:
    """
    Generate a unique identifier (UID) with the given prefix.

    Parameters:
        path (Path): The path to the CSV file containing existing UIDs.
        prefix (str): The prefix to be added to the generated UID.

    Returns:
        str: The generated unique identifier.
    """
    ids = list(read_csv(path)["ID/Passwort"])
    while True:
        new_id = f"{prefix}{randint(100, 999)}"
        if new_id not in ids:
            return new_id


def add_doctor(doctor_data: dict):
    """
    Add a new doctor to the system.

    Args:
        doctor_data (dict): A dictionary containing the doctor's data, including username, password, and availability.
    """
    updateJson(paths["passwords"], {doctor_data["username"]: mhash(doctor_data["password"])})
    updateJson(paths["doctors"]["free"], {doctor_data["username"]: doctor_data["availability"]})
    doctor_data["password"] = gen_UID(paths["doctors"]["csv"], 'A')
    doctor_data.pop("availability")
    appendCSV(paths["doctors"]["csv"], doctor_data.values())


def add_patient(patient_data: dict):
    """
    Add a new patient to the system.

    Args:
        patient_data (dict): A dictionary containing the patient's data.
    """
    updateJson(paths["passwords"], {patient_data["username"]: mhash(patient_data["password"])})
    patient_data["password"] = gen_UID(paths["patients"]["csv"], 'P')
    appendCSV(paths["patients"]["csv"], patient_data.values())


def username_exists(username: str) -> bool:
    """
    Check if a username exists in the loaded JSON passwords.

    Args:
        username (str): The username to check.

    Returns:
        bool: True if the username exists, False otherwise.
    """
    return username in loadJson(paths["passwords"]).keys()


def update_password(new_password: str, bundle: dict):
    """
    Update the password for a user in the passwords JSON file.

    Args:
        new_password (str): The new password to be set.
        bundle (dict): A dictionary containing user information.
    """
    updateJson(paths["passwords"], {bundle["username"]: mhash(new_password)}, replace=True)


def check_login(username: str, password: str, bundle: dict) -> bool:
    """
    Check if the provided username and password are valid.

    Args:
        username (str): The username to check.
        password (str): The password to check.
        bundle (dict): A dictionary to store additional information.

    Returns:
        bool: True if the login is successful, False otherwise.
    """
    if not username_exists(username):
        return False
    elif not mcheck(password, loadJson(paths["passwords"])[username]):
        return False
    else:
        bundle["username"] = username
        return True


alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"


def random_chars(n: int) -> str:
    """
    Generate a random string of length n using characters from the alphabet.

    Args:
        n (int): The length of the random string to generate.

    Returns:
        str: A random string of length n.
    """
    return "".join(choices(population=alphabet, k=n))


def generate_code(bundle: dict):
    """
    Generates a code and adds it to the given bundle dictionary if it doesn't already exist.

    Args:
        bundle (dict): The dictionary to store the generated code.

    Returns:
        str: The generated code.
    """
    if "code" not in bundle:
        bundle["code"] = random_chars(8)
    return bundle["code"]


def check_code(code: str, bundle: dict):
    """
    Check if the provided code matches the code stored in the bundle.

    Args:
        code (str): The code to be checked.
        bundle (dict): The bundle containing the stored code.

    Returns:
        bool: True if the provided code matches the stored code, False otherwise.
    """
    return bundle["code"] == code
