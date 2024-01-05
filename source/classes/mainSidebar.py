import customtkinter as ctk
from PIL import Image

from source.classes.settings import SettingsWindow

sidebar_width = 160

class MainSidebar(ctk.CTkFrame):
    """
    The MainSidebar class represents the main sidebar of the GUI application.
    It contains buttons and labels for navigation and functionality.

    Attributes:
        logo_image (ctk.CTkImage): The logo image displayed in the sidebar.
        home_image (ctk.CTkImage): The home button image displayed in the sidebar.
        event_image (ctk.CTkImage): The event button image displayed in the sidebar.
        settings_image (ctk.CTkImage): The settings button image displayed in the sidebar.
        logout_image (ctk.CTkImage): The logout button image displayed in the sidebar.
        logo_label (ctk.CTkLabel): The label displaying the logo and text in the sidebar.
        home_button (ctk.CTkButton): The button for navigating to the home page.
        book_event_button (ctk.CTkButton): The button for booking an event.
        settings_button (ctk.CTkButton): The button for accessing the settings.
        settings_window (SettingsWindow): The window for the settings.
        logout_button (ctk.CTkButton): The button for logging out.
        copyright_label (ctk.CTkLabel): The label displaying the copyright information.
        current_state (int): The current state of the sidebar.

    Methods:
        __init__(self, master: ctk.CTk): Initializes the MainSidebar object.
        reset(self): Resets the current state of the sidebar.
        update(self): Updates the appearance of the sidebar based on the current state.
        set_grid(self): Sets the grid layout for the sidebar widgets.
        settings(self): Opens the settings window or brings it to focus if already open.
        logout(self): Logs out the user and resets the sidebar and main view.
        home(self): Navigates to the home page.
        book_event(self): Navigates to the event booking page.
    """
    
    def __init__(self, master: ctk.CTk):
        """
        Initializes the MainSidebar object.

        Args:
            master (ctk.CTk): The master widget for the sidebar.
        """
        super().__init__(master=master, width=sidebar_width, corner_radius=0)

        self.grid_rowconfigure(3, weight=1)
        self.current_state = 0
        
        # load images (light and dark)
        image_path = "assets"
        self.logo_image = ctk.CTkImage(light_image=Image.open(f"{image_path}/zahn_logo_light.png"),
                                       dark_image=Image.open(f"{image_path}/zahn_logo_dark.png"), size=(26, 26))
        self.home_image = ctk.CTkImage(light_image=Image.open(f"{image_path}/home_light.png"),
                                       dark_image=Image.open(f"{image_path}/home_dark.png"))
        self.event_image = ctk.CTkImage(light_image=Image.open(f"{image_path}/event_light.png"),
                                        dark_image=Image.open(f"{image_path}/event_dark.png"))
        self.settings_image = ctk.CTkImage(light_image=Image.open(f"{image_path}/settings_light.png"),
                                           dark_image=Image.open(f"{image_path}/settings_dark.png"))
        self.logout_image = ctk.CTkImage(light_image=Image.open(f"{image_path}/logout_light.png"),
                                         dark_image=Image.open(f"{image_path}/logout_dark.png"))
        
        # widgets
        self.logo_label = ctk.CTkLabel(self, text="  Zahn Planer", image=self.logo_image, compound="left", font=ctk.CTkFont(size=20, weight="bold"))
        self.home_button = ctk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Startseite",
                                         fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                         image=self.home_image, anchor="w", command=self.home)
        self.book_event_button = ctk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Termin buchen",
                                               fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                               image=self.event_image, anchor="w", command=self.book_event)
        self.settings_button = ctk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Einstellungen",
                                             fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                             image=self.settings_image, anchor="w", command=self.settings)
        self.settings_window = None
        self.logout_button = ctk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Abmelden",
                                           fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                           image=self.logout_image, anchor="w", command=self.logout)
        self.copyright_label = ctk.CTkLabel(self, corner_radius=0, height=20, width=190, text="© 2023 Adrian Lösch, Lukas Klassen",
                                            font=ctk.CTkFont(size=9, weight="normal"), text_color="gray50", fg_color=("gray80", "gray20"))
        self.set_grid()
        
    def reset(self):
        """
        Resets the current state of the sidebar to 0 (Home).
        """
        self.current_state = 0
        self.update()
        
    def update(self):
        """
        Updates the appearance of the sidebar based on the current state.
        Current state 0: home button is active, book event button is inactive
        Current state 1: home button is inactive, book event button is active
        """
        if self.current_state == 0:
            self.home_button.configure(fg_color=("gray75", "gray25"))
            self.book_event_button.configure(fg_color="transparent")
        elif self.current_state == 1:
            self.home_button.configure(fg_color="transparent")
            self.book_event_button.configure(fg_color=("gray75", "gray25"))
        
    def set_grid(self):
        """
        Sets the grid layout for the sidebar widgets.
        """
        self.logo_label.grid(row=0, column=0, padx=15, pady=(20, 20))
        self.home_button.grid(row=1, column=0, sticky="ew")
        self.book_event_button.grid(row=2, column=0, sticky="ew")
        self.settings_button.grid(row=4, column=0, sticky="ew")
        self.logout_button.grid(row=5, column=0, sticky="ew")
        self.copyright_label.grid(row=6, column=0)
        
    def settings(self):
        """
        Opens the settings window or brings it to focus if already open.
        """
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow()     # create window if its None or destroyed
        elif self.settings_window.state() == "iconic":
            self.settings_window.deiconify()    # bring back window if its minimized
        else:
            self.settings_window.focus()
    
    def logout(self):
        """
        Logs out the user and resets the sidebar and main view then navigates to the login page (initial grid).
        """
        self.reset()
        if self.settings_window is None or not self.settings_window.winfo_exists():
            pass
        else:
            print("test")
            self.settings_window.destroy()
        self.grid_forget()
        self.nametowidget(".").home.grid_forget()
        self.nametowidget(".").booking.grid_forget()
        self.nametowidget(".").initial_grid()
        
    def home(self):
        """
        Navigates to the home page.
        """
        self.current_state = 0
        self.update()
        # ungrid booking, grid home
        self.nametowidget(".").booking.grid_forget()
        self.nametowidget(".").home_grid()
    
    def book_event(self):
        """
        Navigates to the event booking page.
        """
        self.current_state = 1
        self.update()
        # ungrid home, grid booking
        self.nametowidget(".").home.grid_forget()
        self.nametowidget(".").booking_grid()
        
        