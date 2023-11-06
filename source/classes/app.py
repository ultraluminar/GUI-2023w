import customtkinter as ctk

from source.classes.mainLoginFrame import MainLoginFrame
from source.classes.mainRegisterFrame import MainRegisterFrame

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
        self.grid_columnconfigure(0, weight=1)

        self.main_frame_login = MainLoginFrame(master=self, pwds=self.pwds)
        self.main_frame_register = MainRegisterFrame(master=self, pwds=self.pwds)


        # initial packing
        self.main_frame_login.grid(sticky="nsew")

        # run
        self.bind("<Return>", self.main_frame_login.login_form_frame.try_login)