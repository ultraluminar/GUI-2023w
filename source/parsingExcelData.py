from pandas import read_excel

df = read_excel("source/data.xlsx", sheet_name="Stamm-Patienten", header=3, usecols="C:G")
df.to_csv(path_or_buf="source/patients.csv")

df = read_excel("source/data.xlsx", sheet_name="Zahnärzte", header=2, usecols="B:E")
df.to_csv(path_or_buf="source/doctors.csv")

df = read_excel("source/data.xlsx", sheet_name="Kosten und Behandlungsdauer", header=3, usecols="B:G")
df.rename(columns={"Unnamed: 5": "gesetzlicher Anteil", "Unnamed: 6": "privater Anteil"}, inplace=True)

old_problem = ""
for i, isnan in enumerate(df["Dentale Problematik"].isna()):
    if not isnan:
        old_problem = df["Dentale Problematik"][i]
    else:
        df["Dentale Problematik"][i] = old_problem

df.to_csv(path_or_buf="source/costs.csv")
