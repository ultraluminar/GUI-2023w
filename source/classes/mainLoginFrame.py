import customtkinter as ctk

from source.classes.loginFormFrame import LoginFormFrame

# variables
initial_width = 800
initial_height = 800

class MainLoginFrame(ctk.CTkScrollableFrame):
    def __init__(self, master: ctk.CTk):
        super().__init__(master=master, width=initial_width, height=initial_height, corner_radius=0, fg_color="transparent")

        self.font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")

        # login widgets
        self.login_form_frame = LoginFormFrame(self)

        self.login_page_heading = ctk.CTkLabel(self, text="Anmelden oder Registrieren", font=self.font24)
        self.login_register_note = ctk.CTkLabel(self, text="Sie haben noch kein Konto?")
        self.login_register_button = ctk.CTkButton(self, text="Registrieren", command=self.linkToRegister)

        self.set_pack()

    def set_pack(self):
        self.login_page_heading.pack(pady=(10, 20))
        self.login_form_frame.pack()
        self.login_register_note.pack(pady=(20, 0))
        self.login_register_button.pack(pady=(5, 20))

    def linkToRegister(self):
        main_register_frame = self.nametowidget(".!ctkframe2.!canvas.!mainregisterframe")
        self.grid_forget()
        self.login_form_frame.reset()
        main_register_frame.grid(row=0, column=1, sticky="nsew")
        self.nametowidget(".").bind("<Return>", main_register_frame.register_form_frame.try_patient_register)


