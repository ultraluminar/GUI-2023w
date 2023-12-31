import customtkinter as ctk

from CTkToolTip import CTkToolTip

from source.classes.registerFormFrame import RegisterFormFrame


# variables
initial_width = 800
initial_height = 500

class MainRegisterFrame(ctk.CTkScrollableFrame):
    """
    A custom frame for the main registration page.

    This frame contains the registration form, page heading, login note, and login button.

    Methods:
        set_pack(self): Packs the widgets in the frame.
        linkToLogin(self): Handles the click event of the login button.
    """
    def __init__(self, master: ctk.CTk, bundle: dict):
        """
        Initializes the MainRegisterFrame.
        
        Args:
            master (ctk.CTk): The master widget.
            bundle (dict): A dictionary containing data bundle.
        """
        super().__init__(master=master, width=initial_width, height=initial_height, corner_radius=0, fg_color="transparent")

        self.font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        self.data_bundle = bundle

        self.register_form_frame = RegisterFormFrame(self, self.data_bundle)

        self.register_page_heading = ctk.CTkLabel(self, text="Anmelden oder Registrieren", font=self.font24)
        self.register_login_note = ctk.CTkLabel(self, text="Sie haben schon ein Konto?")
        self.register_login_button = ctk.CTkButton(self, text="Login", command=self.linkToLogin)

        self.set_pack()


        CTkToolTip(self.register_login_button, message="Klicken um zur Login-Seite zu gelangen", alpha=0.8)

    def set_pack(self):
        """
        Pack the widgets in the frame.

        This method sets the packing order of the widgets in the frame.
        """
        self.register_page_heading.pack(pady=(10, 20))
        self.register_form_frame.pack()
        self.register_login_note.pack(pady=(20, 0))
        self.register_login_button.pack(pady=(5, 20))

    def linkToLogin(self):
        """
        Link to the login page.

        This method is called when the login button is clicked.
        It retrieves the main login frame, hides the current frame, and shows the main login frame.
        It also binds the Return key to the login form's try_login method.
        """
        main_login_frame = self.nametowidget(".!ctkframe.!canvas.!mainloginframe")
        self.grid_forget()
        main_login_frame.grid(row=0, column=1, sticky="nsew")
        self.nametowidget(".").bind("<Return>", self.nametowidget(".!ctkframe.!canvas.!mainloginframe.!loginformframe").try_login)