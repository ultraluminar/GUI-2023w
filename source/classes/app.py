import customtkinter as ctk

from source.classes.mainLoginFrame import MainLoginFrame
from source.classes.mainRegisterFrame import MainRegisterFrame
from source.classes.login_sidebar import LoginSidebar

from source.classes.main_sidebar import MainSidebar
from source.classes.tmp_main import Main

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

# variables
initial_width = 800
initial_height = 600

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("login")
        self.geometry(f"{initial_width}x{initial_height}")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # login
        self.login_sidebar = LoginSidebar(self)
        self.main_frame_login = MainLoginFrame(self)
        self.main_frame_register = MainRegisterFrame(self)


        self.initial_grid()

        # run
        self.bind("<Return>", self.main_frame_login.login_form_frame.try_login)

    def initial_grid(self):
        self.login_sidebar.grid(row=0, column=0, sticky="nsew")
        self.main_frame_login.grid(row=0, column=1, sticky="nsew")
        
    def main_grid(self, username: str):
        # main
        self.main_sidebar = MainSidebar(self, username=username)
        self.main_main = Main(self, username=username)
        self.main_sidebar.grid(row=0, column=0, sticky="nsew")
        self.main_main.grid(row=0, column=1, sticky="nsew")
