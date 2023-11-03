import customtkinter as ctk
from json import load

from test.classes.loginFormFrame import LoginFormFrame
from test.classes.registerFormFrame import RegisterFormFrame

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# variables
initial_width = 800
initial_height = 500
input_width = 160
json_file_path = "test/pwd.json"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # load json
        with open(json_file_path, "r") as filestream:
            self.pwds: dict = load(filestream)


        self.title("login")
        self.geometry(f"{initial_width}x{initial_height}")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_frame_login = ctk.CTkScrollableFrame(
            self, width=initial_width, height=initial_height, corner_radius=0, fg_color="transparent")
        self.main_frame_register = ctk.CTkScrollableFrame(
            self, width=initial_width, height=initial_height, corner_radius=0, fg_color="transparent")

        # login widgets
        self.login_form_frame = LoginFormFrame(master=self.main_frame_login, pwds=self.pwds)

        self.login_page_heading = ctk.CTkLabel(
            self.main_frame_login, text="Anmelden oder Registrieren",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"))
        self.login_register_note = ctk.CTkLabel(self.main_frame_login, text="Sie haben noch kein Konto?")
        self.login_register_button = ctk.CTkButton(self.main_frame_login, text="Registrieren", command=self.linkToRegister)

        # register widgets
        self.register_form_frame = RegisterFormFrame(self.main_frame_register, pwds=self.pwds)

        self.register_page_heading = ctk.CTkLabel(
            self.main_frame_register, text="Anmelden oder Registrieren", font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"))
        self.register_login_note = ctk.CTkLabel(self.main_frame_register, text="Sie haben schon ein Konto?")
        self.register_login_button = ctk.CTkButton(self.main_frame_register, text="Login", command=self.linkToLogin)

        self.set_pack()

        # initial packing
        self.main_frame_login.grid(row=0, column=0, sticky="nsew")

        # run
        self.bind("<Return>", self.login_form_frame.try_login)


    def set_pack(self):
        self.login_page_heading.pack(pady=(10, 20))
        self.login_form_frame.pack()
        self.login_register_note.pack(pady=(20, 0))
        self.login_register_button.pack(pady=(5, 20))

        self.register_page_heading.pack(pady=(10, 20))
        self.register_form_frame.pack()
        self.register_login_note.pack(pady=(20, 0))
        self.register_login_button.pack(pady=(5, 20))

    def linkToRegister(self):
        self.main_frame_login.grid_forget()
        self.main_frame_register.grid(row=0, column=0, sticky="nsew")

    def linkToLogin(self):
        self.main_frame_register.grid_forget()
        self.main_frame_login.grid(row=0, column=0, sticky="nsew")
