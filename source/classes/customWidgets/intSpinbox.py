import tkinter as tk
import customtkinter as ctk

from PIL import Image

class IntSpinbox(ctk.CTkFrame):
    """
    A custom spinbox widget that allows the user to input and adjust an integer value within a specified range.

    Methods:
        add(): Increments the value of the spinbox by the specified step.
        subtract(): Decrements the value of the spinbox by the specified step.
        get() -> int: Returns the current value of the spinbox.
        set(value: int): Sets the value of the spinbox to the specified value.
    """

    def __init__(self, master, width: int = 140, height: int = 32, step: int = 1, from_: int = 1, to: int = 32):
        """
        Initializes the IntSpinbox widget.
        
        Args:
            master (tk.Widget): The parent widget.
            width (int, optional): The width of the spinbox widget. Defaults to 140.
            height (int, optional): The height of the spinbox widget. Defaults to 32.
            step (int, optional): The increment or decrement step value. Defaults to 1.
            from_ (int, optional): The minimum value of the spinbox. Defaults to 1.
            to (int, optional): The maximum value of the spinbox. Defaults to 32.
        """
        super().__init__(master=master, width=width, height=height)

        self.step = step
        self.from_ = from_
        self.to = to
        
        # load icon images
        image_path = "assets/"
        self.plus_image = ctk.CTkImage(Image.open(f"{image_path}plus.png"), size=(10, 10))
        self.minus_image = ctk.CTkImage(Image.open(f"{image_path}minus.png"), size=(10, 10))

        self.entryInt = tk.IntVar(value=1)

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = ctk.CTkButton(
            self, image=self.minus_image, text="", width=height-6, height=height-6, command=self.subtract)
        self.entry = ctk.CTkEntry(
            self, width=width-(2*height), height=height-6, border_width=0, textvariable=self.entryInt, state="disabled")
        self.add_button = ctk.CTkButton(
            self, image=self.plus_image, text="", width=height-6, height=height-6, command=self.add)

        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

    def add(self):
        """
        Increments the value of the spinbox by the specified step.
        """
        value = self.entryInt.get()
        if value < self.to:
            self.entryInt.set(value + self.step)

    def subtract(self):
        """
        Decrements the value of the spinbox by the specified step.
        """
        value = self.entryInt.get()
        if value > self.from_:
            self.entryInt.set(value - self.step)

    def get(self) -> int:
        """
        Returns the current value of the spinbox.

        Returns:
            int: The current value of the spinbox.
        """
        return self.entryInt.get()

    def set(self, value: int):
        """
        Sets the value of the spinbox to the specified value.

        Args:
            value (int): The value to set the spinbox to.
        """
        self.entryInt.set(value=value)