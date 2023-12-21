import customtkinter as ctk
import tkinter as tk

from PIL import Image, ImageTk

class Booking (ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        
        # variables
        self.days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
        self.times = ["8:00", "9:00", "10:00", "11:00", "12:00", "13:00",
                      "14:00", "15:00", "16:00", "17:00"]
        
        # tk variables
        self.day = tk.StringVar(value="")
        
        # window icon
        self.iconpath = ImageTk.PhotoImage(Image.open("assets/zahn_logo_dark.png", "r"))
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
        # TODO: Implement dynamic duration
        self.duration = f"_Stunden und _Minuten"
        self.main_subheading_label = ctk.CTkLabel(self, text=f"Ihre Behandlung dauert {self.duration}")
        self.cancel_button = ctk.CTkButton(self, text="Abbrechen", command=self.cancel)
        self.save_button = ctk.CTkButton(self, text="Speichern", command=self.save)
        
        # choose day subframe widgets
        self.choose_day_frame = ctk.CTkFrame(self)
        self.choose_day_heading_label = ctk.CTkLabel(self.choose_day_frame, text="Tag auswählen", font=self.font20, anchor="w", width=400)
        self.choose_day_subheading_label = ctk.CTkLabel(self.choose_day_frame, text="Bitte wählen Sie einen Tag aus", anchor="w", width=400)
        self.choose_day_combobox = ctk.CTkComboBox(self.choose_day_frame, values=self.days, variable=self.day)

        # choose time subframe widgets
        self.choose_time_frame = ctk.CTkFrame(self)
        self.choose_time_heading_label = ctk.CTkLabel(self.choose_time_frame, text="Uhrzeit auswählen", font=self.font20, anchor="w", width=400)
        self.choose_time_subheading_label = ctk.CTkLabel(self.choose_time_frame, text="Bitte wählen Sie eine Uhrzeit aus", anchor="w", width=400)
        self.choose_time_combobox = ctk.CTkComboBox(self.choose_time_frame, values=self.times, variable=self.day)

        self.set_choose_day_frame_grid()
        self.set_choose_time_frame_grid()
        self.set_main_grid()

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

    def cancel(self):
        # TODO: Implement cancel
        # self.destroy()
        pass

    def save(self):
        # TODO: Implement save
        pass   
        