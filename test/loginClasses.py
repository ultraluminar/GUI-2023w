import tkinter as tk
import customtkinter as ctk

from bcrypt import hashpw, checkpw, gensalt
from json import load, dump

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# variables
initial_width = 800
initial_height = 500
input_width = 160
json_file_path = "test/pwd.json"

# load json
with open(json_file_path, "r") as filestream:
    logindata: dict = load(filestream)


# logic
def mhash(plain: str) -> str:
    return hashpw(plain.encode(), gensalt()).decode()


def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "":
        return
    if username not in logindata.keys():
        print("username doesn't exist")
        return
    if password == "":
        return

    if checkpw(password.encode(), logindata[username].encode()):
        print("logged in")
    else:
        print("password incorrect")


def register():
    username = username_entry.get()
    password = password_entry.get()

    if username == "":
        print("no username given")
        return
    if username in logindata.keys():
        print("username already exists")
        return
    if password == "":
        print("no password given")
        return
    if " " in password:
        print("password may not contain spaces")
        return
    if len(password) < 6:
        print("password must have at least 6 characters")
        return

    print(mhash(password))
    logindata[username] = mhash(password)

    with open(json_file_path, "w") as filestream:
        dump(logindata, filestream, indent=4)


def linkToRegister():
    login_form_frame.pack_forget()
    login_register_note.pack_forget()
    login_register_button.pack_forget()
    register_frame.pack()
    register_login_note.pack(pady=(20, 0))
    register_login_button.pack(pady=(5, 0))


def linkToLogin():
    register_frame.pack_forget()
    register_login_note.pack_forget()
    register_login_button.pack_forget()
    login_form_frame.pack()
    login_register_note.pack(pady=(20, 0))
    login_register_button.pack(pady=(5, 0))


# window
window = ctk.CTk()
window.title("login")
window.geometry(f"{initial_width}x{initial_height}")

class LoginFormFrame(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk):
        super().__init__(master)

        self.font15 = ctk.CTkFont(family="Segoe UI", size=15)
        # self.font13 = ctk.CTkFont(family="Segoe UI", size=13)

        self.heading = ctk.CTkLabel(master=self, text="Bitte melden sie sich an", font=self.font15)
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Benutzername", width=input_width)
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Passwort", width=input_width, show="•")
        self.login_button = ctk.CTkButton(self, text="Einloggen", command=self.login)

        self.set_grid()

    def set_grid(self):
        self.heading.grid(row=1, column=0, pady=(20, 0), padx=0, sticky="n")
        self.username_entry.grid(row=2, column=0, pady=(20, 0), padx=50, sticky="n")
        self.password_entry.grid(row=3, column=0, pady=(15, 0), padx=50, sticky="n")
        self.login_button.grid(row=4, column=0, pady=(25, 30), padx=50, sticky="n")

# tk variables
register_health_ensurance_var = tk.StringVar()
register_dental_problem_var = tk.StringVar()
register_teeth_count_string = tk.StringVar(value="Anzahl zu behandelnder Zähne")
register_teeth_count_var = tk.IntVar()

# WIDGETS
login_page_heading = ctk.CTkLabel(window, text="Anmelden oder Registrieren",
                                  font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"))
login_form_frame = LoginFormFrame(master=window)

# login widgets
login_register_note = ctk.CTkLabel(window, text="Sie haben noch kein Konto?")
login_register_button = ctk.CTkButton(window, text="Registrieren", command=linkToRegister)

# register widgets
register_frame = ctk.CTkFrame(window)
register_heading = ctk.CTkLabel(register_frame, text="Bitte hier registrieren",
                                font=ctk.CTkFont(family="Segoe UI", size=15))
new_username_entry = ctk.CTkEntry(register_frame, placeholder_text="Benutzername", width=input_width)
new_password_entry = ctk.CTkEntry(register_frame, placeholder_text="Passwort", show="•", width=input_width)
confirm_new_password_entry = ctk.CTkEntry(register_frame, placeholder_text="Passwort bestätigen", show="•",
                                          width=input_width)
health_insurance_combobox = ctk.CTkComboBox(register_frame, values=["gesetzlich", "freiwillig gesetzlich", "privat"],
                                            variable=register_health_ensurance_var, state="readonly", width=input_width)
health_insurance_combobox.set("Krankenkassenart")
dental_problem_combobox = ctk.CTkComboBox(register_frame, values=["Karies klein", "Karies groß", "Teilkrone", "Krone",
                                                                  "Wurzelbehandlung"],
                                          variable=register_dental_problem_var, state="readonly", width=input_width)
dental_problem_combobox.set("Dentale Problematik")
teeth_count_entry = ctk.CTkEntry(register_frame, textvariable=register_teeth_count_string, state="disabled",
                                 width=input_width)
teeth_count_slider = ctk.CTkSlider(register_frame, variable=register_teeth_count_var, from_=1, to=32,
                                   number_of_steps=31,
                                   command=lambda count: register_teeth_count_string.set(str(int(count))),
                                   width=input_width)
register_button = ctk.CTkButton(register_frame, text="Registrieren", command=register)

register_login_note = ctk.CTkLabel(window, text="Sie haben schon ein Konto?")
register_login_button = ctk.CTkButton(window, text="Login", command=linkToLogin)

register_heading.grid(row=1, column=0, pady=(20, 0), padx=0, sticky="n")
new_username_entry.grid(row=2, column=0, pady=(20, 0), padx=50, sticky="n")
new_password_entry.grid(row=3, column=0, pady=(15, 0), padx=50, sticky="n")
confirm_new_password_entry.grid(row=4, column=0, pady=(10, 0), padx=50, sticky="n")
health_insurance_combobox.grid(row=5, column=0, pady=(15, 0), padx=50, sticky="n")
dental_problem_combobox.grid(row=6, column=0, pady=(15, 0), padx=50, sticky="n")
teeth_count_entry.grid(row=7, column=0, pady=(15, 0), padx=50, sticky="n")
teeth_count_slider.grid(row=8, column=0, pady=(15, 0), padx=50, sticky="n")
register_button.grid(row=9, column=0, pady=(25, 30), padx=50, sticky="n")

# packing
login_page_heading.pack(pady=(10, 20))
login_form_frame.pack()
login_register_note.pack(pady=(20, 0))
login_register_button.pack(pady=(5, 0))

# run
window.bind("<Return>", login)
window.mainloop()