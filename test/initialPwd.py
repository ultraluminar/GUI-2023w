from csv import DictReader
from json import dump

csv_file_path = "patients.csv"
json_file_path = "test/initialPwd.json"
initial_pwd = {}


from pandas import read_csv
from bcrypt import checkpw
from loginA import mhash

df = read_csv(csv_file_path, usecols=["Patient", "ID/Passwort"])
df["ID/Passwort"].map(lambda pwd: mhash(pwd))
print(df.to_string())

exit(1)

with open(csv_file_path, "r") as filestream:
    patients_data = DictReader(filestream)
    for row in patients_data:   
        initial_pwd[row["Patient"]] = row["ID/Passwort"]
    
with open(json_file_path, "w") as filestream:
    dump(initial_pwd, filestream, indent=4, ensure_ascii=False)