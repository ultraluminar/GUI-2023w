import customtkinter as ctk
from tkinter import StringVar
from PIL import Image, ImageTk

from source.utils import center_window

class Frame(ctk.CTkFrame):
    """
    A custom frame class that represents a GUI frame with a label, entry, and button.

    Args:
        master: The master widget.
        font: The font to be used for the label, entry, and button.

    Attributes:
        font (Font): The font used for the label, entry, and button.
        auth_service (AuthService): The authentication service instance.
        copy_image (CTkImage): The image used for the copy button.
        var (StringVar): The variable used to store the entry text.
        label (CTkLabel): The label widget.
        entry (CTkEntry): The entry widget.
        button (CTkButton): The button widget.
        
    Methods:
        copy_code: Copies the current code to the clipboard.
    """

    def __init__(self, master, font):
        super().__init__(master=master)
        self.font = font
        self.auth_service = self.nametowidget(".").auth_service
        
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

        self.auth_service.generate_code()
        self.var.set(self.auth_service.code)

    def copy_code(self, event=None):
        """
        Copies the current code to the clipboard.

        Args:
            event (Event, optional): The event that triggered the copy action.
        """
        self.clipboard_clear()
        self.clipboard_append(self.auth_service.code)
        self.button.configure(fg_color=("#26a31d", "#369130"), hover_color=("#1d8017", "#2c7527"))


class Admin(ctk.CTkToplevel):
    """
    A custom toplevel window that lets you manage the admin code. 

    Attributes:
        title (str): The title of the Admin window.
        iconpath (str): The path to the icon image file.
        font24 (ctk.CTkFont): The font used in the Admin window.
        frame (Frame): The main frame of the Admin window.

    Methods:
        __init__(self, master): Initializes the Admin window.
    """

    def __init__(self, master):
        super().__init__(master=master)

        self.title("Freischalt-code")
        
        # window icon
        self.iconpath = ImageTk.PhotoImage(Image.open("assets/zahn_icon.png", "r"))
        self.wm_iconbitmap()
        self.after(0, lambda: self.iconphoto(False, self.iconpath))

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        center_window(self, 400, 200)

        self.font24 = ctk.CTkFont(family="Segoe UI", size=30, weight="bold")

        self.frame = Frame(master=self, font=self.font24)
        self.frame.grid()
