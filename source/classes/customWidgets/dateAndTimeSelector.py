import tkinter as tk
import customtkinter as ctk

class DateAndTimeSelector(ctk.CTkFrame):
    def __init__(self, master, width: int = 400, height: int = 150):
        super().__init__(master=master, width=width, height=height)
        
        # fonts
        self.font20 = ctk.CTkFont(family="Segoe UI", size=20, weight="bold")
        
        # variables
        self.day_from = tk.StringVar()
        self.day_to = tk.StringVar()
        self.time_from = tk.StringVar()
        self.time_to = tk.StringVar()
        
        self.weekdays = ["Mo", "Di", "Mi", "Do", "Fr"]
        self.hours = ["6:00 Uhr", "7:00 Uhr", "8:00 Uhr", "9:00 Uhr", "10:00 Uhr", "11:00 Uhr", "12:00 Uhr", "13:00 Uhr", "14:00 Uhr", "15:00 Uhr", "16:00 Uhr", "17:00 Uhr", "18:00 Uhr", "19:00 Uhr", "20:00 Uhr"]
        
        # day subframe
        self.day_frame = ctk.CTkFrame(self)
        # labels
        self.day_label = ctk.CTkLabel(self.day_frame, text="Tage", font=self.font20)
        self.day_from_label = ctk.CTkLabel(self.day_frame, text="Von")
        self.day_to_label = ctk.CTkLabel(self.day_frame, text="Bis")
        # comboboxes
        self.day_from_combobox = ctk.CTkComboBox(self.day_frame, width=60, values=self.weekdays, variable=self.day_from, state="readonly")
        self.day_to_combobox = ctk.CTkComboBox(self.day_frame, width=60, values=self.weekdays, variable=self.day_to, state="readonly")
        
        # time subframe
        self.time_frame = ctk.CTkFrame(self)
        # labels
        self.time_label = ctk.CTkLabel(self.time_frame, text="Uhrzeit", font=self.font20)
        self.time_from_label = ctk.CTkLabel(self.time_frame, text="Von")
        self.time_to_label = ctk.CTkLabel(self.time_frame, text="Bis")
        # comboboxes
        self.time_from_combobox = ctk.CTkComboBox(self.time_frame, width=100, values=self.hours, variable=self.time_from, state="readonly")
        self.time_to_combobox = ctk.CTkComboBox(self.time_frame, width=100, values=self.hours, variable=self.time_to, state="readonly")
        

        # grid day subframe
        self.day_label.grid(row=0, column=0, columnspan=4, pady=(6, 0))
        self.day_from_label.grid(row=1, column=0, pady=10, padx=(6, 0))
        self.day_from_combobox.grid(row=1, column=1, pady=10, padx=(5, 0))
        self.day_to_label.grid(row=1, column=2, pady=10, padx=(5, 0))
        self.day_to_combobox.grid(row=1, column=3, pady=10, padx=(5, 10))

        # grid time subframe
        self.time_label.grid(row=0, column=0, columnspan=4, pady=(6, 0))
        self.time_from_label.grid(row=1, column=0, pady=10, padx=(6, 0))
        self.time_from_combobox.grid(row=1, column=1, pady=10, padx=(5, 0))
        self.time_to_label.grid(row=1, column=2, pady=10, padx=(5, 0))
        self.time_to_combobox.grid(row=1, column=3, pady=10, padx=(5, 10))
        
        # grid main
        self.day_frame.grid(row=0, column=0, pady=10, padx=10)
        self.time_frame.grid(row=0, column=1, pady=10, padx=10)
        
        
    def get(self):
        # TODO implement a get method, that returns the selected data in usable format
        pass
    