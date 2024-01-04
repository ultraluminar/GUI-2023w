import customtkinter as ctk
from tkinter import IntVar
from tkinter.font import Font

class InfoBanner(ctk.CTkFrame):
    def __init__(self, master, text: str, seconds: int = 10):
        super().__init__(master, fg_color=("#3ba156", "#458556"))

        self.duration = seconds*12

        self.grid_columnconfigure((0, 2), weight=1)
        self.font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")


        self.label = ctk.CTkLabel(self, text=text, font=self.font24)
        self.bar = ctk.CTkProgressBar(self)

        self.label.grid(row=0, column=1, sticky="nsew", pady=(20, 5), padx=20)
        self.bar.grid(row=1, column=1, sticky="nsew", pady=(0, 20), padx=20)

    def show(self):
        tick = 1000 // 12
        progress = self.duration
        for _ in range(self.duration):
            self.after(tick)
            progress -= 1
            self.bar.set(progress)
            self.update()
        self.destroy()
