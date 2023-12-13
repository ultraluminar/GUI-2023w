from pathlib import Path

import customtkinter as ctk
from tkinter import StringVar
from datetime import datetime

from source.auth_util import loadJson


class Frame(ctk.CTkFrame):
    def __init__(self, master, font):
        super().__init__(master=master)
        self.font = font
        self.auth_service = self.nametowidget(".").auth_service

        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.var = StringVar(value="")

        self.label = ctk.CTkLabel(master=self, text="Current Code", font=self.font, width=250)
        self.entry = ctk.CTkEntry(master=self, textvariable=self.var, justify="center",
                                  state="readonly", font=self.font, width=250)
        self.bar = ctk.CTkProgressBar(master=self, determinate_speed=0.1)
        self.button = ctk.CTkButton(master=self, text="X", command=self.copy_code, width=50)

        self.label.grid(row=0, column=0, columnspan=2, sticky="nswe", pady=(10, 0), padx=10)
        self.entry.grid(row=1, column=0, sticky="nswe", pady=(10, 0), padx=(10, 0))
        self.button.grid(row=1, column=1, sticky="nswe", pady=(10, 0), padx=(5, 10))
        self.bar.grid(row=2, column=0, columnspan=2, sticky="nswe", pady=10, padx=10)

        self.updater()

    def copy_code(self, event=None):
        self.clipboard_clear()
        self.clipboard_append(self.auth_service.code)

    def updater(self):
        self.auth_service.generate_code()
        self.var.set(self.auth_service.code)

        #second = datetime.now().second
        #if second == 0:
        #    self.var.set(self.otp.now())
        #self.bar.set(second / 30)
        #self.after(10_000, self.updater)


class Admin(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master=master)

        self.title("")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.initial_width = 400
        self.initial_height = 200

        self.startpos_x = round((self.screen_width / 2) - (self.initial_width / 2))
        self.startpos_y = round((self.screen_height / 2) - (self.initial_height / 2))

        self.geometry(f"{self.initial_width}x{self.initial_height}+{self.startpos_x}+{self.startpos_y}")

        self.font24 = ctk.CTkFont(family="Segoe UI", size=30, weight="bold")

        self.frame = Frame(master=self, font=self.font24)
        self.frame.grid()
