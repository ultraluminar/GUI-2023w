import customtkinter as ctk

from source.classes.loginFormFrame import LoginFormFrame
from CTkToolTip import CTkToolTip

# variables
initial_width = 800
initial_height = 800

class MainLoginFrame(ctk.CTkScrollableFrame):
    """
    Represents the main login frame of the application.

    This frame contains the login form, a heading, a note, and a register button.
    Users can enter their login credentials or register for a new account.

    Methods:
        __init__(self, master: ctk.CTk): Initializes the MainLoginFrame.
        set_pack(self): Packs the widgets in the frame.
        linkToRegister(self): Handles the click event of the register button.
    """

    def __init__(self, master: ctk.CTk, bundle: dict):
        """
        Initializes the MainLoginFrame.
        
        Args:
            master (ctk.CTk): The master widget.
            bundle (dict): A dictionary containing data bundle.
        """
        super().__init__(master=master, width=initial_width, height=initial_height, corner_radius=0, fg_color="transparent")

        self.font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        self.data_bundle = bundle

        # login widgets
        self.login_form_frame = LoginFormFrame(self, self.data_bundle)

        self.login_page_heading = ctk.CTkLabel(self, text="Anmelden oder Registrieren", font=self.font24)
        self.login_register_note = ctk.CTkLabel(self, text="Sie haben noch kein Konto?")
        self.login_register_button = ctk.CTkButton(self, text="Registrieren", command=self.linkToRegister)

        self.set_pack()

        # tooltips
        CTkToolTip(self.login_register_button, message="Klicken um zur Registrierungs-Seite zu gelangen", alpha=0.8)

    def set_pack(self):
        """
        Packs the widgets in the MainLoginFrame.
        """
        self.login_page_heading.pack(pady=(10, 20))
        self.login_form_frame.pack()
        self.login_register_note.pack(pady=(20, 0))
        self.login_register_button.pack(pady=(5, 20))

    def linkToRegister(self):
        """
        Handles the click event of the register button.
        It hides the login frame, resets it and displays the register frame.
        It also binds the Return key to the register form's try_patient_register method.
        """
        main_register_frame = self.nametowidget(".!ctkframe2.!canvas.!mainregisterframe")
        self.grid_forget()
        self.login_form_frame.reset()
        main_register_frame.grid(row=0, column=1, sticky="nsew")
        self.nametowidget(".").bind("<Return>", main_register_frame.register_form_frame.try_patient_register)
