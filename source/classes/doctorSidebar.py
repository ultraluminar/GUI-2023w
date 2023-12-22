import customtkinter as ctk
from PIL import Image

from source.classes.settings import SettingsWindow

sidebar_width = 160

class DoctorSidebar(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk):
        super().__init__(master=master, width=sidebar_width, corner_radius=0)

        self.grid_rowconfigure(3, weight=1)
        self.current_state = 0
        
        # load images (light and dark)
        image_path = "assets"
        self.logo_image = ctk.CTkImage(light_image=Image.open(f"{image_path}/zahn_logo_light.png"),
                                       dark_image=Image.open(f"{image_path}/zahn_logo_dark.png"), size=(26, 26))
        self.home_image = ctk.CTkImage(light_image=Image.open(f"{image_path}/home_light.png"),
                                       dark_image=Image.open(f"{image_path}/home_dark.png"))
        self.settings_image = ctk.CTkImage(light_image=Image.open(f"{image_path}/settings_light.png"),
                                           dark_image=Image.open(f"{image_path}/settings_dark.png"))
        self.logout_image = ctk.CTkImage(light_image=Image.open(f"{image_path}/logout_light.png"),
                                         dark_image=Image.open(f"{image_path}/logout_dark.png"))
        
        # widgets
        self.logo_label = ctk.CTkLabel(self, text="  Zahn Planer", image=self.logo_image, compound="left", font=ctk.CTkFont(size=20, weight="bold"))
        self.home_button = ctk.CTkButton(self, corner_radius=0, height=40, border_spacing=10, text="Startseite",
                                         fg_color=("gray75", "gray25"), text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                         image=self.home_image, anchor="w")
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
        
    def set_grid(self):
        self.logo_label.grid(row=0, column=0, padx=15, pady=(20, 20))
        self.home_button.grid(row=1, column=0, sticky="ew")
        self.settings_button.grid(row=4, column=0, sticky="ew")
        self.logout_button.grid(row=5, column=0, sticky="ew")
        self.copyright_label.grid(row=6, column=0)
        
        
    def settings(self):
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow()     # create window if its None or destroyed
        elif self.settings_window.state() == "iconic":
            self.settings_window.deiconify()    # bring back window if its minimized
        else:
            self.settings_window.focus()
    
    
    # hides widgets from the main view and brings back login widgets
    def logout(self):
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
        