import customtkinter as ctk

from source.classes.customWidgets.dateAndTimeSelector import DateAndTimeSelector

class TimeSelector(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        
        #variables
        window_width = 600
        window_height = 500
        
        # initialize window
        self.geometry(f"{window_width}x{window_height}")
        self.title("Behandlungszeiten Selektor")
        self.resizable(False, True)
        self.attributes("-topmost", 1) # forces window to be on always on top
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.columnconfigure(1, weight=1)
        
        # fonts
        self.font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        
        # time selector scrollable frame
        self.frame = ctk.CTkScrollableFrame(self, width=window_width, corner_radius=0, fg_color="transparent")
        
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
        