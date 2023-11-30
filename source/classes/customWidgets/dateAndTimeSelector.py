import tkinter as tk
import customtkinter as ctk

from datetime import time
from dateutil.relativedelta import weekday

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

        self.day_from.trace_add("write", self.day_updater)
        self.time_from.trace_add("write", self.time_updater)
        
        self.weekdays = ["Mo", "Di", "Mi", "Do", "Fr"]
        self.hours = [f"{x}:00 Uhr" for x in range(8, 18+1)]
        
        self.destroy_color = ("#C22741", "#CC455C")
        self.destroy_hover_color = ("#911d30", "#872f3e")
        
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
        
        # main widgets
        self.destroy_button = ctk.CTkButton(self, width=32, fg_color=self.destroy_color, hover_color=self.destroy_hover_color, text="x", command=lambda: self.nametowidget(".!timeselector").destroy_selector(self))

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
        self.time_frame.grid(row=0, column=1, pady=10, padx=(10, 0))
        self.destroy_button.grid(row=0, column=2, pady=10, padx=10)
        
    def day_updater(self, *args):
        days_from = self.day_from.get()
        days_to = self.day_to.get()

        if not days_from:   # der callback wird warumauchimmer 2x aufgerufen mit 1x days_from = ""
            return

        index = self.weekdays.index(days_from)
        new_values = self.weekdays[index:]
        self.day_to_combobox.configure(values=new_values)
        if days_to and days_to not in new_values:
            self.day_to.set("")


    def time_updater(self, *args):
        time_from = self.time_from.get()
        time_to = self.time_to.get()

        if not time_from:   # der callback wird warumauchimmer 2x aufgerufen mit 1x time_from = ""
            return

        index = self.hours.index(time_from)
        new_values = self.hours[index:]
        self.time_to_combobox.configure(values=new_values)
        if time_to and time_to not in new_values:
            self.time_to.set("")

    def get(self) -> dict:
        # TODO implement a get method, that returns the selected data in usable format
        day_range = range(self.weekdays.index(self.day_from.get()), self.weekdays.index(self.day_to.get()) + 1)

        start_time = int(self.time_from.get().split(':')[0])
        stop_time = int(self.time_to.get().split(':')[0])

        return {weekday(day): (start_time, stop_time) for day in day_range}
        