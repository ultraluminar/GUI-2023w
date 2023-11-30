import customtkinter as ctk

from dateutil.relativedelta import weekday

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
        self.destroy()
    
    def save(self):
        dicts = [selector.get() for selector in self.selectors]
        week = [weekday(x) for x in range(5)]

        ranges_combined = {key: [dic[key] for dic in dicts if key in dic] for key in week}
        print(ranges_combined)
    
    def add_selector(self):
        self.selectors.append(DateAndTimeSelector(self.frame))
        self.add_button.pack_forget()
        self.selectors[-1].pack(pady=(20, 0))
        self.add_button.pack(pady=(10, 20))
        
    def destroy_selector(self, selector):
        selector.pack_forget()
        self.selectors.remove(selector)