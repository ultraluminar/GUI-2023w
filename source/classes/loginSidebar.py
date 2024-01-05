import customtkinter as ctk
from PIL import Image

from source.classes.admin import Admin
from CTkToolTip import CTkToolTip

# variables
sidebar_width = 160

class LoginSidebar(ctk.CTkFrame):
    """
    A custom login sidebar widget for a GUI application.

    This class represents a sidebar widget that contains a logo, admin button, exit button, and a copyright label.
    It provides functionality to display a pop-up window when the admin button is clicked, and to quit the application
    when the exit button is clicked.

    Methods:
        pop_up(event=None): Displays the admin pop-up window.
        set_grid(): Sets the grid layout for the widgets in the sidebar.
    """

    def __init__(self, master: ctk.CTk, bundle: dict):
        """
        Initializes an instance of the LoginSidebar class.

        Args:
            master (ctk.CTk): The master widget.
            bundle (dict): A dictionary containing data bundle.
        """
        super().__init__(master=master, width=sidebar_width, corner_radius=0)
        self.admin: ctk.CTkToplevel = None

        self.grid_rowconfigure(1, weight=1)
        self.data_bundle = bundle

        # load images (light and dark)
        image_path = "assets/"
        self.logo_image = ctk.CTkImage(light_image=Image.open(f"{image_path}zahn_logo_light.png"),
                                       dark_image=Image.open(f"{image_path}zahn_logo_dark.png"), size=(26, 26))
        self.exit_image = ctk.CTkImage(light_image=Image.open(f"{image_path}logout_light.png"),
                                       dark_image=Image.open(f"{image_path}logout_dark.png"))
        self.key_image = ctk.CTkImage(light_image=Image.open(f"{image_path}key_light.png"),
                                       dark_image=Image.open(f"{image_path}key_dark.png"))
        
        # widgets
        self.logo_label = ctk.CTkLabel(self, text="  Zahn Planer", image=self.logo_image, compound="left", font=ctk.CTkFont(size=20, weight="bold"))
        self.admin_button = ctk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Admin",
                                       fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                       image=self.key_image, anchor="w", command=self.pop_up)
        self.exit_button = ctk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Beenden",
                                         fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                         image=self.exit_image, anchor="w", command=self.quit)
        self.copyright_label = ctk.CTkLabel(self, corner_radius=0, height=20, width=190, text="© 2023 Adrian Lösch, Lukas Klassen",
                                            font=ctk.CTkFont(size=9, weight="normal"), text_color="gray50", fg_color=("gray80", "gray20"))
        
        self.set_grid()

        # tooltips
        CTkToolTip(self.admin_button, message="Klicken um Freischaltcode zu erhalten", alpha=0.8)
        CTkToolTip(self.exit_button, message="Klicken um das Programm zu schließen", alpha=0.8)


    def pop_up(self, event=None):
        """
        Displays the admin pop-up window.

        This method is called when the admin button is clicked. It creates a new instance of the Admin class
        and displays the pop-up window. If the pop-up window already exists, it brings it back to focus.

        Args:
            event (Event, optional): The event that triggered the pop-up. Defaults to None.
        """
        if self.admin is None or not self.admin.winfo_exists():
            self.admin = Admin(self, self.data_bundle)     # create window if its None or destroyed
            self.after(0, self.admin.focus)
        elif self.admin.state() == "iconic":
            self.admin.deiconify()    # bring back window if its minimized
        else:
            self.admin.focus()   

    def set_grid(self):
        """
        Sets the grid layout for the widgets in the sidebar.

        This method configures the grid layout for the logo label, admin button, exit button, and copyright label and shows them.
        """
        self.logo_label.grid(row=0, column=0, padx=15, pady=(20, 10))
        self.admin_button.grid(row=2, column=0, sticky="ew")
        self.exit_button.grid(row=3, column=0, sticky="ew")
        self.copyright_label.grid(row=4, column=0, padx=0)
