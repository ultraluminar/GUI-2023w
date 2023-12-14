import customtkinter as ctk

from source.classes.mainLoginFrame import MainLoginFrame
from source.classes.mainRegisterFrame import MainRegisterFrame
from source.classes.login_sidebar import LoginSidebar

from source.classes.main_sidebar import MainSidebar
from source.classes.mainBookingFrame import MainBookingFrame

from source.auth_util import AuthenticationService

from PIL import ImageTk, Image

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")



class App(ctk.CTk):
    def __init__(self):
        super().__init__()


        self.title("Zahn Planer")

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.initial_width = round(self.screen_width * 0.75)
        self.initial_height = round(self.screen_height * 0.75)

        self.startpos_x = round((self.screen_width/2) - (self.initial_width/2))
        self.startpos_y = round((self.screen_height/2) - (self.initial_height/2))

        # window icon
        self.iconpath = ImageTk.PhotoImage(Image.open("assets/zahn_logo_dark.png", "r"))
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)

        self.geometry(f"{self.initial_width}x{self.initial_height}+{self.startpos_x}+{self.startpos_y}")

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

        # run
        self.bind("<Return>", self.main_frame_login.login_form_frame.try_login)

    def initial_grid(self):
        self.login_sidebar.grid(row=0, column=0, sticky="nsew")
        self.main_frame_login.grid(row=0, column=1, sticky="nsew")
        self.bind("<Return>", self.nametowidget(".!ctkframe.!canvas.!mainloginframe.!loginformframe").try_login)
        
    def main_grid(self):
        # main
        self.main_sidebar.grid(row=0, column=0, sticky="nsew")
        self.main_main.grid(row=0, column=1, sticky="nsew")
