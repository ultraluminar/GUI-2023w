import customtkinter as ctk
import tkinter as tk

from PIL import ImageTk, Image
import logging

from source.auth_util import update_password, check_login


class SettingsWindow(ctk.CTkToplevel):
    """
    A class representing the settings window of the application.

    This window provides the user with the ability to modify various settings of the application.
    These settings include changing the color scheme of the application and updating the user's password.

    Methods:
        __init__: Initializes the SettingsWindow class and sets up the window.
        update_error_label: Updates the error label with the provided message.
        change_password: Changes the user's password.
        update_appearance: Updates the appearance of the application.
    """
    def __init__(self, bundle: dict):
        """
    Initialize the SettingsWindow class.

    This method sets up the window, initializes variables, loads the window icon, sets the window title,
    and initializes the authentication service. It also sets up the fonts and widgets used in the window,
    including labels, frames, and buttons. It also sets up the grid layout of the window and binds the
    Return key to the password changing function.

    Variables:
        inner_width: The width of the inner window.
        error_string: A string variable that holds any error messages.

    Widgets:
        main_label: The main label of the settings window.
        design_frame: The frame for the design settings.
        design_label: The label for the design settings.
        appearance_mode_optionemenu: The option menu for changing the appearance mode.
        change_password_frame: The frame for the password change settings.
        change_password_label: The label for the password change settings.
        old_password_entry: The entry field for the old password.
        new_password_entry: The entry field for the new password.
        error_label: The label for displaying error messages.
        change_password_button: The button for initiating a password change.
    """
        super().__init__()

        # variables
        self.inner_width = 400
        self.error_string = tk.StringVar(value="")
        self.data_bundle = bundle

        # window icon
        self.iconpath = ImageTk.PhotoImage(Image.open("assets/zahn_icon.png", "r"))
        self.wm_iconbitmap()
        self.after(300, lambda: self.iconphoto(False, self.iconpath))

        # initialize window
        self.title("Einstellungen")
        self.resizable(False, False)

        # fonts
        self.font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        self.font20 = ctk.CTkFont(family="Segoe UI", size=20, weight="bold")

        # widgets
        self.main_label = ctk.CTkLabel(self, text="Einstellungen", font=self.font24)

        # design subframe widgets
        self.design_frame = ctk.CTkFrame(self)
        self.grid_rowconfigure((0, 1), weight=1)
        self.design_label = ctk.CTkLabel(self.design_frame, text="Farbdesign ändern", font=self.font20, anchor="w", width=self.inner_width)
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.design_frame, values=["Light", "Dark", "System"],
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.set("System")

        # password change subframe widgets
        self.change_password_frame = ctk.CTkFrame(self)
        self.grid_rowconfigure((0, 1), weight=1)
        self.change_password_label = ctk.CTkLabel(self.change_password_frame, text="Passwort ändern", font=self.font20, anchor="w", width=self.inner_width)
        self.old_password_entry = ctk.CTkEntry(self.change_password_frame, placeholder_text="Altes Passwort", show="•")
        self.new_password_entry = ctk.CTkEntry(self.change_password_frame, placeholder_text="Neues Passwort", show="•")
        self.error_label = ctk.CTkLabel(self.change_password_frame, text_color="red", textvariable=self.error_string)
        self.change_password_button = ctk.CTkButton(self.change_password_frame, text="Passwort ändern", command=self.change_password)

        # design subframe grid
        self.design_label.grid(row=0, column=0, padx=20, pady=(15, 20))
        self.appearance_mode_optionemenu.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        # password change subframe grid
        self.change_password_label.grid(row=0, column=0, padx=20, pady=(15, 20))
        self.old_password_entry.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        self.new_password_entry.grid(row=2, column=0, columnspan=2, pady=(0, 20))
        self.change_password_button.grid(row=4, column=0, columnspan=2, pady=(0, 20))

        # main label and subframe packing on window
        self.main_label.grid(column=0, row=0, pady=(10, 15), padx=20, sticky="nsew")
        self.design_frame.grid(column=0, row=1, pady=(0, 15), padx=20, sticky="nsew")
        self.change_password_frame.grid(column=0, row=2, pady=(0, 20), padx=20, sticky="nsew")

        # binding Return Key to password changing function
        self.bind("<Return>", self.change_password)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """
        Change the appearance mode of the application.

        Args:
            new_appearance_mode (str): The new appearance mode to set.
        """
        current = ctk.get_appearance_mode()
        if current != "System" and new_appearance_mode != current:
            ctk.set_appearance_mode(new_appearance_mode)
            self.after(1, self.lift)

    def change_password(self, event=None):
        """
        Change the user's password.

        This method retrieves the old and new passwords from the respective entry fields, checks for any errors
        such as empty fields or incorrect old password, and updates the password if there are no errors. It also
        updates the border color of the entry fields and the error label text based on the presence of errors.

        Args:
            event (Event, optional): The event that triggered the password change. Defaults to None.
        """
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()

        default_color = ("#979DA2", "#565B5E")

        entrys = [self.old_password_entry, self.new_password_entry]

        entry_map = [
            [self.old_password_entry, old_password == "", "Bitte geben sie ihr altes Passwort ein"],
            [self.old_password_entry, not check_login(self.data_bundle["username"], old_password, self.data_bundle), "Das alte Passwort ist falsch"],
            [self.new_password_entry, new_password == "", "Bitte geben sie ihr neues Passwort ein"],
            [self.new_password_entry, old_password == new_password, "Das neue Passwort darf nicht gleich dem alten sein"]
        ]

        error_entrys = []
        error_messages = []
        for entry, is_problem, error_string in entry_map:
            if is_problem:
                error_entrys.append(entry)
                logging.warning(error_string)
                error_messages.append(error_string)
                break

        for entry in entrys:
            entry.configure(border_color=("red" if entry in error_entrys else default_color))
        if error_messages:  # not empty
            self.error_string.set("\n".join(error_messages))  # set error label text
            self.error_label.grid(row=3, column=0, columnspan=2, pady=(0, 10), sticky="nsew")
        else:
            self.error_label.grid_forget()

        if error_entrys:  # not empty:
            return

        update_password(new_password, self.data_bundle["username"])
        self.old_password_entry.configure(border_color="green")
        self.new_password_entry.configure(border_color="green")
        print("password changed")