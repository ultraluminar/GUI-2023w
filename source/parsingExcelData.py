from pandas import read_excel, read_csv
from bcrypt import hashpw, gensalt
from json import dump

def behandelt_analyse(df):

    for index, row in df.iterrows():
        behandelt = row['behandelt'].lstrip("nur ").split(" und ")

        for art in ["privat", "gesetzlich", "freiwillig gesetzlich"]:
            df.at[index, art] = art in behandelt

    # df.drop('behandelt', axis=1, inplace=True)
    return df

file_path = "source/data/data.xlsx"
new_file_directory_path = "source/data"

# parsing the inital data excel file to csv files
# parsing the patients table
df_patients = read_excel(io=file_path, sheet_name="Stamm-Patienten", header=3, usecols="C:G")
df_patients.to_csv(path_or_buf=f"{new_file_directory_path}/patients.csv", index=False)

# hashing passwords
df_patients["Hash"] = df_patients["ID/Passwort"].map(lambda plain: hashpw(plain.encode(), gensalt()).decode())
df_passwords = df_patients[["Patient", "Hash"]]
password_dict = df_passwords.to_dict(orient="records")
json_data = {item["Patient"]: item["Hash"] for item in password_dict}
with open(f"{new_file_directory_path}/pwd.json", "w", encoding="utf-8") as filestream:
    dump(json_data, filestream, indent=4, ensure_ascii=False)

# parsing the doctors table
df_doctors = read_excel(io=file_path, sheet_name="Zahnärzte", header=2, usecols="B:E")
df_doctors = behandelt_analyse(df_doctors)
df_doctors.to_csv(path_or_buf=f"{new_file_directory_path}/doctors.csv", index=False)

# parsing the costs table
df_costs = read_excel(io=file_path, sheet_name="Kosten und Behandlungsdauer", header=3, usecols="B:G")
# replacing column names that are missing in the excel file
df_costs.rename(columns={"Unnamed: 5": "gesetzlicher Anteil", "Unnamed: 6": "privater Anteil"}, inplace=True)

# adding the "Dentale Problematik" column in every row instead of only the first
dental_problem = ""
for index, is_nan in enumerate(df_costs["Dentale Problematik"].isna()):
    if not is_nan:
        dental_problem = df_costs["Dentale Problematik"][index]
    else:
        # FIXME: SettingWithCopyWarning:
        #   A value is trying to be set on a copy of a slice from a DataFrame
        #   See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
        #   df_costs["Dentale Problematik"][index] = dental_problem
        #   ansatz: df_costs.loc[:, ("Dentale Problematik", index)] = dental_problem
        df_costs["Dentale Problematik"][index] = dental_problem

df_costs.to_csv(path_or_buf=f"{new_file_directory_path}/costs.csv", index=False)