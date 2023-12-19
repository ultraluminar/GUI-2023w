import customtkinter as ctk
import tkinter as tk

from source.classes.customWidgets.calenderWeekView import WeekCalenderView

class (ctk.CTkFrame):
    def __init__(self, master: ctk.CTk):
        super().__init__(master=master)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # variables
        
        # fonts
        
        # main widgets
        self.heading_label = ctk.CTkLabel(self, text="Termin auswählen", font=self.font24)
        self.sub_heading_label = ctk.CTkLabel(self, text="Sehen sie sich den Kalender an und buchen sie einen Termin.")
        self.last_week_button = ctk.CTkButton(self, text="last", command=self.last_week)
        self.next_week_button = ctk.CTkButton(self, text="next", command=self.next_week)
        self.week_calender_view = WeekCalenderView(self)
        self.book_button = ctk.CTkButton(self, text="Buchen", command=self.booking_view)
        
    def set_main_grid(self):
        self.heading_label.grid(column=1, row=0, pady=(20, 0), sticky="nsew")
        self.sub_heading_label.grid(column=1, row=1, sticky="nsew")
        self.last_week_button.grid(column=0, row=0, rowspan=2, pady=20, sticky="e", padx=(20, 0))
        self.next_week_button.grid(column=2, row=0, rowspan=2, pady=20, sticky="w", padx=(0, 20))
        self.week_calender_view.grid(column=0, columnspan=3, row=2, pady=20, sticky="nsew")
        self.book_button.grid(column=0, columnspan=3, row=3, pady=20, sticky="e", padx=(0, 20))
        
    def reset(self):
        WeekCalenderView.reset()
        
    def last_week(self):
        pass
        # WeekCalenderView.last_week()
        
    def next_week(self):
        pass
        # WeekCalenderView.next_week()
    
    def booking_view(self):
        pass