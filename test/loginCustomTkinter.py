import tkinter as tk
import customtkinter as ctk

from bcrypt import hashpw, checkpw, gensalt
from json import load, dump

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# variables
initial_width = 800
initial_height = 500
json_file_path = "test/pwd.json"

# load json
with open(json_file_path, "r") as filestream:
    logindata: dict = load(filestream)

# logic
def mhash(plain: str, salt: bytes = gensalt()) -> str:
    return hashpw(plain.encode(), salt).decode()

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

# window
window = ctk.CTk()
window.title("login")
window.geometry(f"{initial_width}x{initial_height}")

# tk variables
username_var = tk.StringVar()
password_var = tk.StringVar()

# widgets
login_page_heading = ctk.CTkLabel(window, text="Anmelden oder Registrieren")
login_frame = ctk.CTkFrame(window)
login_heading = ctk.CTkLabel(login_frame, text="Bitte melden sie sich an")
login_heading.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
username_entry = ctk.CTkEntry(login_frame, placeholder_text="Benutzername")
username_entry.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
password_entry = ctk.CTkEntry(login_frame, placeholder_text="Passwort", show="•")
password_entry.grid(row=3, column=0, pady=(20, 0), padx=20, sticky="n")
login_button = ctk.CTkButton(login_frame, text="Einloggen", command=login)
login_button.grid(row=4, column=0, pady=20, padx=20, sticky="n")

register_button = ctk.CTkButton(window, text="Registrieren", command=register)

# packing
login_page_heading.pack(pady=(10, 20))
login_frame.pack()
register_button.pack(pady=(30, 0))

# run
window.bind("<Return>", login)
window.mainloop()
