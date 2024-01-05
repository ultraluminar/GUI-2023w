import customtkinter as ctk

from source.classes.mainLoginFrame import MainLoginFrame
from source.classes.mainRegisterFrame import MainRegisterFrame
from source.classes.loginSidebar import LoginSidebar

from source.classes.mainSidebar import MainSidebar
from source.classes.doctorSidebar import DoctorSidebar
from source.classes.mainBookingFrame import MainBookingFrame

from source.utils import center_window
from source.classes.home import HomeFrame
from source.classes.doctorHome import DoctorHome

from PIL import ImageTk, Image

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")



class App(ctk.CTk):
    """
    The main application class that represents the Zahn Planer application.

    Attributes:
        title (str): The title of the application window.
        initial_width (int): The initial width of the application window.
        initial_height (int): The initial height of the application window.
        iconpath (str): The path to the application icon image.
        auth_service (AuthenticationService): An instance of the AuthenticationService class.
        data_bundle (dict): A dictionary to store data used by different frames.

    Methods:
        __init__(): Initializes the App class.
        initial_grid(): Sets up the initial grid layout of the application.
        main_sidebar_grid(): Sets up the grid layout for the main sidebar.
        home_grid(): Sets up the grid layout for the home frame.
        booking_grid(): Sets up the grid layout for the booking frame.
        doctor_grid(): Sets up the grid layout for the doctor frame.
    """

    def __init__(self):
        """
        Initializes the App class by setting up the application window, icon, and initial dimensions.
        It also creates instances of various frames and sets up the initial grid layout.
        """
        super().__init__()

        self.title("Zahn Planer")

        self.initial_width = round(self.winfo_screenwidth() * 0.75)
        self.initial_height = round(self.winfo_screenheight() * 0.75)

        center_window(self, self.initial_width, self.initial_height)

        # window icon
        self.iconpath = ImageTk.PhotoImage(Image.open("assets/zahn_icon.png"))
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.data_bundle = {}

        # login
        self.login_sidebar = LoginSidebar(self, self.data_bundle)
        self.main_frame_login = MainLoginFrame(self, self.data_bundle)
        self.main_frame_register = MainRegisterFrame(self, self.data_bundle)

        # logged in frames
        # patient
        self.main_sidebar = MainSidebar(self, self.data_bundle)
        self.home = HomeFrame(self, self.data_bundle)
        self.booking = MainBookingFrame(self, self.data_bundle)
        # doctor
        self.doctor_sidebar = DoctorSidebar(self, self.data_bundle)
        self.doctor_view = DoctorHome(self, self.data_bundle)

        self.initial_grid()

    def initial_grid(self):
        """
        Sets up the initial grid layout of the application by placing the login sidebar and main login frame.
        It also binds the Enter key to the login form's try_login method.
        """
        self.login_sidebar.grid(row=0, column=0, sticky="nsew")
        self.main_frame_login.grid(row=0, column=1, sticky="nsew")
        self.bind("<Return>", self.main_frame_login.login_form_frame.try_login)

    def main_sidebar_grid(self):
        """
        Sets up the grid layout for the main sidebar by placing it and resets the main sidebar.
        """
        self.main_sidebar.grid(row=0, column=0, sticky="nsew")
        self.main_sidebar.reset()

    def home_grid(self):
        """
        Sets up the grid layout for the home frame by placing and resets the home frame.
        """
        self.home.grid(row=0, column=1, sticky="nsew")
        self.home.reset()

    def booking_grid(self):
        """
        Sets up the grid layout for the booking frame and resets the main booking frame.
        """
        self.booking.grid(row=0, column=1, sticky="nsew")
        self.booking.reset()

    def doctor_grid(self):
        """
        Sets up the grid layout for the doctor view by placing the doctor home frame and the doctor sidebar
        and resets the doctor home frame.
        """
        self.doctor_sidebar.grid(row=0, column=0, sticky="nsew")
        self.doctor_view.grid(row=0, column=1, sticky="nsew")
        self.doctor_view.reset()
