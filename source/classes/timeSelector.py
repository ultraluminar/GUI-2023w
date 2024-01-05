import customtkinter as ctk

from source.classes.customWidgets.dateAndTimeSelector import DateAndTimeSelector

class TimeSelector(ctk.CTkToplevel):
    """
    A custom top-level window for selecting time rules.
    It contains a scrollable frame with a list of DateAndTimeSelector objects.

    Methods:
        __init__(): Initializes the TimeSelector object.
        cancel(): Closes the window.
        save(): Saves the selected time rules.
        add_selector(): Adds a new DateAndTimeSelector object to the window.
        destroy_selector(selector): Removes a DateAndTimeSelector object from the window.
    """

    def __init__(self):
        """
        Initializes the TimeSelector object.

        Sets up the window with initial dimensions, title, and attributes.
        Configures the rows and columns of the window.
        Initializes fonts, scrollable frame, and widgets.
        Packs the widgets into the grid layout.
        """
        super().__init__()

        self.initial_width = 600
        self.initial_height = 500

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.startpos_x = round((self.screen_width / 2) - (self.initial_width / 2))
        self.startpos_y = round((self.screen_height / 2) - (self.initial_height / 2))

        # initialize window
        self.geometry(f"{self.initial_width}x{self.initial_height}+{self.startpos_x}+{self.startpos_y}")

        self.title("Behandlungszeiten Selektor")
        self.resizable(False, True)
        self.attributes("-topmost", 1) # forces window to be on always on top
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.columnconfigure(1, weight=1)
        
        # fonts
        self.font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        
        # time selector scrollable frame
        self.frame = ctk.CTkScrollableFrame(self, width=self.initial_width, corner_radius=0, fg_color="transparent")
        
        # frame widgets
        self.main_label = ctk.CTkLabel(self.frame, text="Behandlungszeiten auswählen", font=self.font24)
        self.selectors = [DateAndTimeSelector(self.frame)]
        self.add_button = ctk.CTkButton(self.frame, text="Zeitraum hinzufügen", command=self.add_selector)
        
        # main widgets
        self.cancel_button = ctk.CTkButton(self, text="Abbrechen", command=self.cancel)
        self.save_button = ctk.CTkButton(self, text="Speichern", command=self.save)
        
        # grid frame
        self.main_label.pack(pady=(20, 0))
        self.selectors[0].pack(pady=(20, 0))
        self.add_button.pack(pady=(10, 20))

        # grid main
        self.frame.grid(row=0, column=0, columnspan=3, sticky="nsw")
        self.cancel_button.grid(row=1, column=0, pady=20, padx=(20, 0), sticky="sw")
        self.save_button.grid(row=1, column=2, pady=20, padx=(0, 20), sticky="es")

    def cancel(self):
        """
        Closes the window.
        """
        self.destroy()
    
    def save(self):
        """
        Saves the selected time rules.

        Retrieves the selected time rules from each DateAndTimeSelector object.
        If any rule is None, the saving process is aborted.
        Passes the rules to the appropriate method in the parent widget.
        Hides the window.
        """
        rules = [selector.get() for selector in self.selectors]
        
        # dont save when inputs faulty
        if any(rule is None for rule in rules): 
            return

        self.nametowidget(".!ctkframe2.!canvas.!mainregisterframe.!registerformframe").doctor_time_selector_saved(rules)
        self.withdraw()
    
    def add_selector(self):
        """
        Adds a new DateAndTimeSelector object to the window.

        Creates a new DateAndTimeSelector object and appends it to the selectors list.
        Rearranges the widgets in the frame and repacks them.
        """
        self.selectors.append(DateAndTimeSelector(self.frame))
        self.add_button.pack_forget()
        self.selectors[-1].pack(pady=(20, 0))
        self.add_button.pack(pady=(10, 20))
        
    def destroy_selector(self, selector):
        """
        Removes a DateAndTimeSelector object from the window.

        Removes the specified DateAndTimeSelector object from the selectors list.
        Forgets the packing of the selector widget.
        
        Args:
            selector (DateAndTimeSelector): The DateAndTimeSelector object to remove.
        """
        selector.pack_forget()
        self.selectors.remove(selector)