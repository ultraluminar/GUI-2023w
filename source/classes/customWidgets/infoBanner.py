import customtkinter as ctk
from tkinter import IntVar
from tkinter.font import Font

class InfoBanner(ctk.CTkFrame):
    """
    A custom widget that displays an information banner with a label and a progress bar.

    Args:
        master: The parent widget.
        bundle (dict): A dictionary containing data bundle.
        seconds (int): The duration of the banner in seconds. Default is 10 seconds.

    Attributes:
        data_bundle (dict): A dictionary containing data bundle.
        duration (int): The duration of the banner in ticks.
        font24 (ctk.CTkFont): The font used for the label.
        label (ctk.CTkLabel): The label widget.
        bar (ctk.CTkProgressBar): The progress bar widget.
    """

    def __init__(self, master, bundle: dict, seconds: int = 10):
        super().__init__(master, fg_color=("#3ba156", "#458556"))

        self.data_bundle = bundle   
        self.duration = seconds*12  

        self.grid_columnconfigure((0, 2), weight=1)

        # font
        self.font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")

        # widgets
        self.label = ctk.CTkLabel(self, font=self.font24)
        self.bar = ctk.CTkProgressBar(self)

        # grid widgets
        self.label.grid(row=0, column=1, sticky="nsew", pady=(20, 5), padx=20)
        self.bar.grid(row=1, column=1, sticky="nsew", pady=(0, 20), padx=20)

    def show(self):
        """
        Displays the information banner.

        This method updates the label text and progresses the progress bar over the duration of the banner.
        """
        self.label.configure(text=f"Termin gebucht: {self.data_bundle['appointment_row'][2]}")

        tick = 1000 // 12   # 12 ticks per second
        progress = 1
        # progress bar animation
        for _ in range(self.duration):
            self.after(tick)
            progress = progress - 1/self.duration
            self.bar.set(progress)
            self.update()
