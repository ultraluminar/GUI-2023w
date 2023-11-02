import tkinter as tk
from tkinter import ttk

from bcrypt import hashpw, checkpw, gensalt
from json import load, dump

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
    username = username_var.get()
    password = password_var.get()
    
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
    username = username_var.get()
    password = password_var.get()
    
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
window = tk.Tk()
window.title("login")
window.geometry(f"{initial_width}x{initial_height}")

# tk variables
username_var = tk.StringVar()
password_var = tk.StringVar()

# widgets
username_frame = ttk.Frame(window)
username_label = ttk.Label(username_frame, text="Nutzername")
username_entry = ttk.Entry(username_frame, textvariable=username_var)

password_frame = ttk.Frame(window)
password_label = ttk.Label(password_frame, text="Passwort")
password_entry = ttk.Entry(password_frame, textvariable=password_var, show="•")

sign_in_button = ttk.Button(window, text="Anmelden", command=login)
sign_up_button = ttk.Button(window, text="Registrieren", command=register)

username_frame.pack()
username_label.pack(side="left", padx=10)
username_entry.pack(side="left")

password_frame.pack()
password_label.pack(side="left", padx=10)
password_entry.pack(side="left")

sign_in_button.pack(pady=5)
sign_up_button.pack()

# run
window.bind("<Return>", login)
window.mainloop()
