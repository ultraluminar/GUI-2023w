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
    main_frame_login.grid_forget()
    main_frame_register.grid(row=0, column=0, sticky="nsew")


def linkToLogin():
    main_frame_register.grid_forget()
    main_frame_login.grid(row=0, column=0, sticky="nsew")


# window
window = ctk.CTk()
window.title("login")
window.geometry(f"{initial_width}x{initial_height}")
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)


# main scrollableframes
main_frame_login = ctk.CTkScrollableFrame(window, width=initial_width, height=initial_height, corner_radius=0, fg_color="transparent")
main_frame_register = ctk.CTkScrollableFrame(window, width=initial_width, height=initial_height, corner_radius=0, fg_color="transparent")

# login widgets
login_form_frame = LoginFormFrame(main_frame_login, pwds=logindata)

login_page_heading = ctk.CTkLabel(
    main_frame_login, text="Anmelden oder Registrieren", font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"))
login_register_note = ctk.CTkLabel(main_frame_login, text="Sie haben noch kein Konto?")
login_register_button = ctk.CTkButton(main_frame_login, text="Registrieren", command=linkToRegister)

# login packing
login_page_heading.pack(pady=(10, 20))
login_form_frame.pack()
login_register_note.pack(pady=(20, 0))
login_register_button.pack(pady=(5, 20))

# register widgets
register_form_frame = RegisterFormFrame(main_frame_register, pwds=logindata)

register_page_heading = ctk.CTkLabel(
    main_frame_register, text="Anmelden oder Registrieren", font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"))
register_login_note = ctk.CTkLabel(main_frame_register, text="Sie haben schon ein Konto?")
register_login_button = ctk.CTkButton(main_frame_register, text="Login", command=linkToLogin)

# register packing
register_page_heading.pack(pady=(10, 20))
register_form_frame.pack()
register_login_note.pack(pady=(20, 0))
register_login_button.pack(pady=(5, 20))

# initial packing
main_frame_login.grid(row=0, column=0, sticky="nsew")

# run
window.bind("<Return>", login_form_frame.try_login)
window.mainloop()