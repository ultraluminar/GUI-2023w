from csv import DictReader
from json import dump

from bcrypt import hashpw, gensalt

csv_file_path = "test/patients.csv"
json_file_path = "test/initialPwd.json"
initial_pwd = {}

def mhash(plain: str, salt: bytes = gensalt()) -> str:
    return hashpw(plain.encode(), salt).decode()

with open(csv_file_path, "r") as filestream:
    patients_data = DictReader(filestream)
    for row in patients_data:   
        initial_pwd[row["Patient"]] = mhash(row["ID/Passwort"])
    
with open(json_file_path, "w") as filestream:
    dump(initial_pwd, filestream, indent=4, ensure_ascii=False)