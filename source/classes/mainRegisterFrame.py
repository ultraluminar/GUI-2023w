import customtkinter as ctk

from source.classes.registerFormFrame import RegisterFormFrame

# variables
initial_width = 800
initial_height = 500

class MainRegisterFrame(ctk.CTkScrollableFrame):
    def __init__(self, master: ctk.CTk):
        super().__init__(master=master, width=initial_width, height=initial_height, corner_radius=0, fg_color="transparent")

        self.font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")

        self.register_form_frame = RegisterFormFrame(self)

        self.register_page_heading = ctk.CTkLabel(self, text="Anmelden oder Registrieren", font=self.font24)
        self.register_login_note = ctk.CTkLabel(self, text="Sie haben schon ein Konto?")
        self.register_login_button = ctk.CTkButton(self, text="Login", command=self.linkToLogin)

        self.set_pack()


    def set_pack(self):
        self.register_page_heading.pack(pady=(10, 20))
        self.register_form_frame.pack()
        self.register_login_note.pack(pady=(20, 0))
        self.register_login_button.pack(pady=(5, 20))

    def linkToLogin(self):
        self.grid_forget()
        self.nametowidget(".!ctkframe.!canvas.!mainloginframe").grid(sticky="nsew")