import customtkinter as ctk

from source.classes.mainLoginFrame import MainLoginFrame
from source.classes.mainRegisterFrame import MainRegisterFrame
from source.classes.login_sidebar import LoginSidebar

from source.classes.main_sidebar import MainSidebar
from source.classes.mainBookingFrame import MainBookingFrame

from source.auth_util import AuthenticationService
from source.utils import center_window

from PIL import ImageTk, Image

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")



class App(ctk.CTk):
    def __init__(self):
        super().__init__()


        self.title("Zahn Planer")

        self.initial_width = round(self.winfo_screenwidth() * 0.75)
        self.initial_height = round(self.winfo_screenheight() * 0.75)

        center_window(self, self.initial_width, self.initial_height)

        # window icon
        self.iconpath = ImageTk.PhotoImage(Image.open("assets/zahn_logo_dark.png"))
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)


        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.auth_service = AuthenticationService()

        # login
        self.login_sidebar = LoginSidebar(self)
        self.main_frame_login = MainLoginFrame(self)
        self.main_frame_register = MainRegisterFrame(self)

        self.main_sidebar = MainSidebar(self)
        self.main_main = MainBookingFrame(self)


        self.initial_grid()

    def initial_grid(self):
        self.login_sidebar.grid(row=0, column=0, sticky="nsew")
        self.main_frame_login.grid(row=0, column=1, sticky="nsew")
        self.bind("<Return>", self.main_frame_login.login_form_frame.try_login)
        
    def main_grid(self):
        # main
        self.main_sidebar.grid(row=0, column=0, sticky="nsew")
        self.main_main.grid(row=0, column=1, sticky="nsew")
