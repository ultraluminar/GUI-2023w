from pandas import read_excel, read_csv
from bcrypt import hashpw, gensalt

file_path = "source/data.xlsx"
new_file_path = "source/pwd.csv"

# parsing the inital data excel file to csv files
# parsing the patients table
df_patients = read_excel(io=file_path, sheet_name="Stamm-Patienten", header=3, usecols="C:G")
df_patients.to_csv(path_or_buf="source/patients.csv", index=False)

# hashing passwords
df_patients["Hash"] = df_patients["ID/Passwort"].map(lambda plain: hashpw(plain.encode(), gensalt()).decode())
df_patients.to_csv(path_or_buf=new_file_path, columns=["Patient", "Hash"], index=False)

# parsing the doctors table
df_doctors = read_excel(io=file_path, sheet_name="Zahnärzte", header=2, usecols="B:E")
df_doctors.to_csv(path_or_buf="source/doctors.csv", index=False)

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

df_costs.to_csv(path_or_buf="source/costs.csv", index=False)