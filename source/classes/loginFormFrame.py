import customtkinter as ctk
import tkinter as tk
import logging

from source.auth_util import username_exists
from pandas import read_csv

class LoginFormFrame(ctk.CTkFrame):
    """
    A custom login form frame that provides a user interface for logging in.

    Attributes:
        font15 (ctk.CTkFont): The font used for the labels and entries.
        input_width (int): The width of the input fields.
        auth_service (AuthService): The authentication service used for login.
        error_string (tk.StringVar): The string variable to store the error message.

    Args:
        master (tk.Widget): The parent widget for this frame.
    """

    def __init__(self, master):
        super().__init__(master=master)

        # fonts
        self.font15 = ctk.CTkFont(family="Segoe UI", size=15)

        # variables
        self.input_width = 200
        self.auth_service = self.nametowidget(".").auth_service
        self.error_string = tk.StringVar(value="")

        # widgets
        self.heading = ctk.CTkLabel(master=self, font=self.font15, text="Bitte melden sie sich an")
        self.username_entry = ctk.CTkEntry(self, width=self.input_width, placeholder_text="Benutzername")
        self.password_entry = ctk.CTkEntry(self, width=self.input_width, placeholder_text="Passwort", show="•")
        self.error_label = ctk.CTkLabel(self, text_color="red", textvariable=self.error_string)
        self.login_button = ctk.CTkButton(self, text="Einloggen", command=self.try_login)

        self.set_grid()

    def set_grid(self):
        """
        Configures the grid layout for the widgets in the frame and displays them.
        """
        self.heading.grid(row=1, column=0, pady=(20, 0), padx=0, sticky="n")
        self.username_entry.grid(row=2, column=0, pady=(20, 0), padx=50, sticky="n")
        self.password_entry.grid(row=3, column=0, pady=(15, 5), padx=50, sticky="n")
        self.login_button.grid(row=5, column=0, pady=(20, 30), padx=50, sticky="n")

    def try_login(self, event=None) -> None:
        """
        Attempts to log in the user.

        Args:
            event (tk.Event, optional): The event that triggered the login attempt. Defaults to None.

        Returns:
            None
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        default_color = ("#979DA2", "#565B5E")

        entrys = [self.username_entry, self.password_entry]

        # check if all entrys are filled
        entry_map = [
            [self.username_entry, username == "", "Kein Benutzername angegeben"],
            [self.username_entry, not username_exists(username), "Benutzername existiert nicht"],
            [self.password_entry, password == "", "Kein Passwort angegeben"],
            [self.password_entry, not self.auth_service.check_login(username, password), "Passwort ist falsch"]
        ]

        error_entrys = []
        error_messages = []
        for entry, is_problem, error_string in entry_map:
            if is_problem:
                error_entrys.append(entry)
                logging.warning(error_string)
                error_messages.append(error_string)
                break  # to prevent seeing errors like "username doesn't exist" on empty username

        # visual error feedback
        for entry in entrys:
            entry.configure(border_color=("red" if entry in error_entrys else default_color))
        if error_messages:  # not empty
            self.error_string.set("\n".join(error_messages))    # set error label text
            self.error_label.grid(row=4, column=0, columnspan=2, pady=(5, 0), padx=50, sticky="n")
        else:
            self.error_label.grid_forget()

        # final check before login
        if error_entrys:  # not empty
            return
        
        self.reset()

        logging.info("logged in")
        # grid forget
        self.nametowidget(".!ctkframe.!canvas.!mainloginframe").grid_forget()
        self.nametowidget(".!loginsidebar").grid_forget()
        # grid
        if self.User_is_doctor(username):   # check if user is doctor
            self.nametowidget(".").doctor_grid()
            return
        self.nametowidget(".").main_sidebar_grid()
        self.nametowidget(".").home_grid()

    def reset(self):
        """
        Resets the input fields and error label.

        Returns:
            None
        """
        # reset entrys for privacy
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.username_entry.configure(border_color=("#979DA2", "#565B5E"))  # reset border color
        self.password_entry.configure(border_color=("#979DA2", "#565B5E"))  
        self.error_label.grid_forget()  # hide error label
        
    def User_is_doctor(self, username: str) -> bool:
        """
        Checks if the given username belongs to a doctor.

        Args:
            username (str): The username to check.

        Returns:
            bool: True if the username belongs to a doctor, False otherwise.
        """
        df = read_csv("data/doctors.csv")
        return username in df["Username"].tolist()   # check if username is in doctors.csv
    