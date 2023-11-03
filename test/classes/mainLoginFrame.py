import customtkinter as ctk

from test.classes.loginFormFrame import LoginFormFrame

# variables
initial_width = 800
initial_height = 800

class MainLoginFrame(ctk.CTkScrollableFrame):
    def __init__(self, master: ctk.CTk, pwds):
        super().__init__(master=master, width=initial_width, height=initial_height, corner_radius=0, fg_color="transparent")

        self.pwds = pwds
        self.font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")

        # login widgets
        self.login_form_frame = LoginFormFrame(master=self, pwds=self.pwds)

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
        self.grid_forget()
        self.nametowidget(".!ctkframe2.!canvas.!mainregisterframe").grid(sticky="nsew")


