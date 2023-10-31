from tkinter import Tk, Frame, Label, Button, Entry, StringVar, Widget
from tkinter.font import Font

from bcrypt import hashpw, checkpw, gensalt
from json import load, dump


def mhash(plain: bytes | str, salt: bytes = gensalt()) -> bytes:
    return hashpw(plain if isinstance(plain, bytes) else plain.encode("utf-8"), salt)


def login(*args):
    entry_user["fg"], entry_pwd["fg"] = "black", "black"
    user, pwd = var_user.get(), var_pwd.get()

    if user == "":
        return
    if user not in logindata.keys():
        entry_user["fg"] = "darkred"
        return
    if pwd == "":
        return

    if checkpw(pwd.encode(), logindata[user].encode()):
        entry_pwd["fg"] = "darkgreen"
    else:
        entry_pwd["fg"] = "darkred"


# --- json setup ---

with open("pwd.json") as filestream:
    logindata: dict = load(filestream)

# --- tkinter ---

window_height = 500
window_width = 900

window = Tk()
window.title("Login System")
window.resizable(False, False)

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))

window.geometry(f'{window_width}x{window_height}+{x_coordinate}+{y_coordinate}')

font_tnr = Font(family="Times New Roman", size=40)
frame_login = Frame()
frame_kwargs = {"master": frame_login, "justify": "center", "font": font_tnr}

label_user = Label(text="Benutzername:", **frame_kwargs)
label_pwd = Label(text="Passwort:", **frame_kwargs)

var_user = StringVar()
var_pwd = StringVar()

entry_user = Entry(width=16, textvariable=var_user, **frame_kwargs)
entry_pwd = Entry(width=16, textvariable=var_pwd, **frame_kwargs, show='•')

button_reg = Button(text="Registrieren", state="disabled", **frame_kwargs)
button_login = Button(text="Login", command=login, **frame_kwargs)

grid_map = [
    [label_user, label_pwd, button_reg],  # column 1
    [entry_user, entry_pwd, button_login]  # column 2
]

for column, rows in enumerate(grid_map):
    for row, widget in enumerate(rows):
        widget.grid(column=column + 1, row=row + 1, ipadx=20, sticky="nsew", padx=5, pady=5)

frame_login.place(anchor="center", relx=0.5, rely=0.5)

window.bind("<Return>", login)
window.mainloop()