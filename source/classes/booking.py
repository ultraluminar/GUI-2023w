import customtkinter as ctk
import tkinter as tk

from PIL import Image, ImageTk
from datetime import time, datetime
from dateutil.relativedelta import relativedelta

from source.classes.timespace import TimeSpace
from source.auth_util import appendCSV, paths


class Booking(ctk.CTkToplevel):
    def __init__(self, timespace: TimeSpace, day_of_week: datetime, bundle: dict):
        super().__init__()

        self.day_of_week = day_of_week
        self.timespace = timespace
        self.duration = bundle["duration_quarters"]
        self.termine = self.timespace.get_termine(self.duration)
        self.data_bundle = bundle
        
        # variables
        self.days_names = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
        self.times = [f"{hour}:00" for hour in range(8, 18)]

        self.days = [string for termin_list, string in zip(self.termine, self.days_names) if termin_list]

        # tk variables
        self.day = tk.StringVar(value="")
        self.hour = tk.StringVar(value="")
        
        # window icon
        self.iconpath = ImageTk.PhotoImage(Image.open("assets/zahn_icon.png"))
        self.wm_iconbitmap()
        self.after(300, lambda: self.iconphoto(False, self.iconpath))
        
        # initialize window
        self.title("Buchung")
        self.resizable(False, False)
        
        self.auth_service = self.nametowidget(".").auth_service
        
        # fonts
        self.font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        self.font20 = ctk.CTkFont(family="Segoe UI", size=20, weight="bold")
        
        # widgets
        self.main_heading_label = ctk.CTkLabel(self, text="Buchung", font=self.font24)
        self.hour_minute = self.convert_to_hour_minute(self.duration)
        hour_string = f"{self.hour_minute[0]} Stunde{'n' if self.hour_minute[0] != 1 else ''}"
        minute_string = f"und {self.hour_minute[1]} Minuten"
        self.main_subheading_label = ctk.CTkLabel(self, text=f"Ihre Behandlung dauert {hour_string} {minute_string if self.hour_minute[1] != 0 else ''}")
        self.cancel_button = ctk.CTkButton(self, text="Abbrechen", command=self.cancel)
        self.save_button = ctk.CTkButton(self, text="Speichern", state="disabled", command=self.save)
        
        # choose day subframe widgets
        self.choose_day_frame = ctk.CTkFrame(self)
        self.choose_day_heading_label = ctk.CTkLabel(self.choose_day_frame, text="Tag auswählen", font=self.font20, anchor="w", width=400)
        self.choose_day_subheading_label = ctk.CTkLabel(self.choose_day_frame, text="Bitte wählen Sie einen Tag aus", anchor="w", width=400)
        self.choose_day_combobox = ctk.CTkComboBox(self.choose_day_frame, values=self.days, variable=self.day, command=self.set_times, state="readonly")

        # choose time subframe widgets
        self.choose_time_frame = ctk.CTkFrame(self)
        self.choose_time_heading_label = ctk.CTkLabel(self.choose_time_frame, text="Uhrzeit auswählen", font=self.font20, anchor="w", width=400)
        self.choose_time_subheading_label = ctk.CTkLabel(self.choose_time_frame, text="Bitte wählen Sie eine Uhrzeit aus", anchor="w", width=400)
        self.choose_time_combobox = ctk.CTkComboBox(self.choose_time_frame, values=self.times, variable=self.hour, state="readonly", command=self.enable_save)

        self.set_choose_day_frame_grid()
        self.set_choose_time_frame_grid()
        self.set_main_grid()

    def enable_save(self, *args):
        if self.day.get() != "" and self.hour.get() != "":
            self.save_button.configure(state="normal")

    def set_main_grid(self):
        self.main_heading_label.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="nsew", columnspan=2)
        self.main_subheading_label.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="nsew", columnspan=2)
        self.choose_day_frame.grid(row=2, column=0, padx=20, pady=(0, 15), sticky="nsew", columnspan=2)
        self.choose_time_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew", columnspan=2)
        self.cancel_button.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="w")
        self.save_button.grid(row=4, column=1, padx=20, pady=(0, 20), sticky="e")
        

    def set_choose_day_frame_grid(self):
        self.choose_day_heading_label.grid(row=0, column=0, padx=20, pady=(15, 0))
        self.choose_day_subheading_label.grid(row=1, column=0, padx=20, pady=(0, 20))
        self.choose_day_combobox.grid(row=2, column=0, columnspan=2, pady=(0, 20))
    
    def set_choose_time_frame_grid(self):
        self.choose_time_heading_label.grid(row=0, column=0, padx=20, pady=(15, 0))
        self.choose_time_subheading_label.grid(row=1, column=0, padx=20, pady=(0, 20))
        self.choose_time_combobox.grid(row=2, column=0, columnspan=2, pady=(0, 20))

    def set_times(self, *args):
        weekday = self.days_names.index(self.day.get())
        times = [termin.strftime("%H:%M") for termin in self.termine[weekday]]
        self.choose_time_combobox.configure(values=times)
        self.hour.set("")
        self.save_button.configure(state="disabled")
        
    # function for converting a count of 15 minutes to a tuple of hours and minutes
    def convert_to_hour_minute(self, count: int) -> tuple:
        hours, minutes = divmod(count, 4)
        return hours, minutes * 15

    def cancel(self):
        self.destroy()

    def save(self):
        weekday = self.days_names.index(self.day.get())
        time_ = datetime.strptime(self.hour.get(), "%H:%M").time()
        start = (self.day_of_week + relativedelta(weekday=weekday)).replace(hour=time_.hour, minute=time_.minute)
        stop = start + relativedelta(minutes=15*self.duration)
        row_data = [
            self.data_bundle["doctor"],
            self.auth_service.username,
            start.strftime("%d-%m-%Y %H:%M"),
            stop.strftime("%d-%m-%Y %H:%M"),
            self.data_bundle["dental_problem"],
            self.data_bundle["tooth_count"],
            self.data_bundle["fill_type"]
        ]
        self.data_bundle["appointment_row"] = row_data
        calendar_view = self.nametowidget(".!mainbookingframe.!calenderviewframe.!weekcalenderview")
        calendar_view.set_week(self.day_of_week)
        calendar_view.add_ex_date(start, stop)
        self.nametowidget(".!mainbookingframe.!calenderviewframe").booking_saved()
        self.destroy()
        