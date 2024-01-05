import customtkinter as ctk
from tkinter import StringVar
from PIL import Image, ImageTk
from CTkToolTip import CTkToolTip

from source.auth_util import generate_code
from source.utils import center_window

class AdminFrame(ctk.CTkFrame):
    """
    A custom frame class that represents a GUI frame with a label, entry, and button.

    Methods:
        copy_code: Copies the current code to the clipboard.
    """

    def __init__(self, master, font, bundle: dict):
        """
        Initializes the AdminFrame widget.
        
        Args:
            master: The parent widget.
            font: The font to be used for the label, entry, and button.
            bundle (dict): A dictionary containing data bundle.
        """
        super().__init__(master=master)
        self.font = font
        self.data_bundle = bundle
        
        image_path = "assets/"
        self.copy_image = ctk.CTkImage(light_image=Image.open(f"{image_path}copy_light.png"), size=(30, 30),
                                       dark_image=Image.open(f"{image_path}copy_dark.png"))

        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.var = StringVar(value="")

        self.label = ctk.CTkLabel(master=self, text="Current Code", font=self.font, width=250)
        self.entry = ctk.CTkEntry(master=self, textvariable=self.var, justify="center",
                                  state="readonly", font=self.font, width=250)
        self.button = ctk.CTkButton(master=self, text="", image=self.copy_image, command=self.copy_code, width=50)

        self.label.grid(row=0, column=0, columnspan=2, sticky="nswe", pady=(10, 0), padx=10)
        self.entry.grid(row=1, column=0, sticky="nswe", pady=10, padx=(10, 0))
        self.button.grid(row=1, column=1, sticky="nswe", pady=10, padx=(5, 10))

        self.var.set(generate_code(self.data_bundle))
        
        # tooltips
        CTkToolTip(self.button, "Klicken um den Code zu kopieren.", alpha=0.8)
        
        # binding
        self.bind("<Enter>", self.copy_code)

    def copy_code(self, *args):
        """
        Copies the current code to the clipboard.
        """
        self.clipboard_clear()
        self.clipboard_append(self.data_bundle["code"])
        self.button.configure(fg_color=("#26a31d", "#369130"), hover_color=("#1d8017", "#2c7527"))


class Admin(ctk.CTkToplevel):
    """
    A custom toplevel window that lets you manage the admin code.
    """

    def __init__(self, master, bundle: dict):
        """
        Initializes the Admin window.
        
        Args:
            master: The parent widget.
            bundle (dict): A dictionary containing data bundle.
        """
        super().__init__(master=master)

        self.title("Freischalt-code")
        self.data_bundle = bundle

        # window icon
        self.iconpath = ImageTk.PhotoImage(Image.open("assets/zahn_icon.png", "r"))
        self.wm_iconbitmap()
        self.after(0, lambda: self.iconphoto(False, self.iconpath))

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        center_window(self, 400, 200)

        self.font24 = ctk.CTkFont(family="Segoe UI", size=30, weight="bold")

        self.frame = AdminFrame(self, self.font24, self.data_bundle)
        self.frame.grid()
