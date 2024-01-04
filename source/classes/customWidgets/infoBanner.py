import customtkinter as ctk
from tkinter import IntVar
from tkinter.font import Font

class InfoBanner(ctk.CTkFrame):
    def __init__(self, master, bundle: dict, seconds: int = 10):
        super().__init__(master, fg_color=("#3ba156", "#458556"))

        self.data_bundle = bundle
        self.duration = seconds*12

        self.grid_columnconfigure((0, 2), weight=1)
        self.font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")


        self.label = ctk.CTkLabel(self, font=self.font24)
        self.bar = ctk.CTkProgressBar(self)

        self.label.grid(row=0, column=1, sticky="nsew", pady=(20, 5), padx=20)
        self.bar.grid(row=1, column=1, sticky="nsew", pady=(0, 20), padx=20)

    def show(self):
        self.label.configure(text=f"Termin gebucht: {self.data_bundle['appointment_row'][2]}")

        tick = 1000 // 12
        progress = 1
        for _ in range(self.duration):
            self.after(tick)
            progress = progress - 1/self.duration
            self.bar.set(progress)
            self.update()
