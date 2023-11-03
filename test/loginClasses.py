import customtkinter as ctk
from json import load

from classes.LoginFormFrame import LoginFormFrame
from classes.RegisterFormFrame import RegisterFormFrame

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
def linkToRegister():
    login_form_frame.pack_forget()
    login_register_note.pack_forget()
    login_register_button.pack_forget()
    register_form_frame.pack()
    register_login_note.pack(pady=(20, 0))
    register_login_button.pack(pady=(5, 0))


def linkToLogin():
    register_form_frame.pack_forget()
    register_login_note.pack_forget()
    register_login_button.pack_forget()
    login_form_frame.pack()
    login_register_note.pack(pady=(20, 0))
    login_register_button.pack(pady=(5, 0))


# window
window = ctk.CTk()
window.title("login")
window.geometry(f"{initial_width}x{initial_height}")



# WIDGETS
login_page_heading = ctk.CTkLabel(
    window, text="Anmelden oder Registrieren", font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"))
login_form_frame = LoginFormFrame(master=window, pwds=logindata)

# login widgets
login_register_note = ctk.CTkLabel(window, text="Sie haben noch kein Konto?")
login_register_button = ctk.CTkButton(window, text="Registrieren", command=linkToRegister)

# register widgets
register_form_frame = RegisterFormFrame(master=window, pwds=logindata)

register_login_note = ctk.CTkLabel(window, text="Sie haben schon ein Konto?")
register_login_button = ctk.CTkButton(window, text="Login", command=linkToLogin)

# packing
login_page_heading.pack(pady=(10, 20))
login_form_frame.pack()
login_register_note.pack(pady=(20, 0))
login_register_button.pack(pady=(5, 0))

# run
window.bind("<Return>", login_form_frame.try_login)
window.mainloop()