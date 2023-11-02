from bcrypt import gensalt, hashpw
from pandas import read_csv

original_file_path = "patients.csv"
new_file_path = "pwd.csv"

df = read_csv(original_file_path, usecols=["Patient", "ID/Passwort"])
df["Hash"] = df["ID/Passwort"].map(lambda plain: hashpw(plain.encode(), gensalt()).decode())
df.to_csv(new_file_path, columns=["Patient", "Hash"], index=False)