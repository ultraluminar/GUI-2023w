import customtkinter as ctk
from PIL import Image

# variables
sidebar_width = 140

class LoginSidebar(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk):
        super().__init__(master=master, width=sidebar_width, corner_radius=0)

        self.grid_rowconfigure(1, weight=1)
        
        
        # load images (light and dark)
        image_path = "assets/"
        self.logo_image = ctk.CTkImage(light_image=Image.open(f"{image_path}zahn_logo_light.png"),
                                       dark_image=Image.open(f"{image_path}zahn_logo_dark.png"), size=(26, 26))
        
        # widgets
        self.logo_label = ctk.CTkLabel(self, text="  Dental Manager", image=self.logo_image, compound="left", font=ctk.CTkFont(size=20, weight="bold"))
        self.exit_button = ctk.CTkButton(self, text="Beenden", command=self.tk.quit)
        
        self.set_grid()
    
    def set_grid(self):
        self.logo_label.grid(row=0, column=0, padx=15, pady=(20, 10))
        self.exit_button.grid(row=2, column=0, padx=15, pady=(10, 20))
