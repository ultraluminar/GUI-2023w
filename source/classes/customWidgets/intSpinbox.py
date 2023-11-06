import tkinter as tk
import customtkinter as ctk

class IntSpinbox(ctk.CTkFrame):
    def __init__(self, master, width: int = 100, height: int = 32, step: int = 1, from_: int = 0, to: int = 32):
        super().__init__(master=master, width=width, height=height)

        self.step = step
        self.from_ = from_
        self.to = to

        self.entryInt = tk.IntVar(value=0)

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = ctk.CTkButton(
            self, text="-", width=height-6, height=height-6, command=self.subtract)
        self.entry = ctk.CTkEntry(
            self, width=width-(2*height), height=height-6, border_width=0, textvariable=self.entryInt, state="disabled")
        self.add_button = ctk.CTkButton(
            self, text="+", width=height-6, height=height-6, command=self.add)

        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

    def add(self):
        value = self.entryInt.get()
        if value < self.to:
            self.entryInt.set(value + self.step)

    def subtract(self):
        value = self.entryInt.get()
        if value > self.from_:
            self.entryInt.set(value - self.step)

    def get(self) -> int:
        return self.entryInt.get()

    def set(self, value: int):
        self.entryInt.set(value=value)