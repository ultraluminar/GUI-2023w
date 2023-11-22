import customtkinter as ctk

from source.classes.customWidgets.dateAndTimeSelector import DateAndTimeSelector

class TimeSelector(ctk.CTkToplevel):
    def __init__(self):
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
        self.selector_1 = DateAndTimeSelector(self.frame)
        
        # main widgets
        self.cancel_button = ctk.CTkButton(self, text="Abbrechen", command=self.cancel)
        self.save_button = ctk.CTkButton(self, text="Speichern", command=self.save)
        
        # grid frame
        self.main_label.pack(pady=(20, 0))
        self.selector_1.pack(pady=(20, 0))

        # grid main
        self.frame.grid(row=0, column=0, columnspan=3, sticky="nsw")
        self.cancel_button.grid(row=1, column=0, pady=20, padx=(20, 0), sticky="sw")
        self.save_button.grid(row=1, column=2, pady=20, padx=(0, 20), sticky="es")

    def cancel(self):
        pass
    
    def save(self):
        pass
        