import customtkinter as ctk

from source.classes.customizeTreatmentFrame import TreatmentFrame

class MainBookingFrame(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk):
        super().__init__(master=master, corner_radius=0, fg_color="transparent")
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # widgets for progression bar
        self.progression_bar_frame = ctk.CTkFrame(self, corner_radius=14)
        self.progression_bar_frame.columnconfigure((0, 5), weight=1)
        
        self.treatment_button = ctk.CTkButton(self.progression_bar_frame, corner_radius=14, text="Behandlung")
        self.doctor_button = ctk.CTkButton(self.progression_bar_frame, corner_radius=14, text="Zahnarzt")
        self.appointment_button = ctk.CTkButton(self.progression_bar_frame, corner_radius=14, text="Termin")
        self.finished_button = ctk.CTkButton(self.progression_bar_frame, corner_radius=14, text="Fertig")
        
        self.reset_progression_bar()
        
        # main frames
        self.treatment_frame = TreatmentFrame(self)
        
        self.set_progression_bar_grid()
        self.set_main_grid()
        
        
    def set_main_grid(self):
        self.progression_bar_frame.grid(column=0, row=0, sticky="new", padx=20, pady=20)
        self.treatment_frame.grid(column=0, row=1, sticky="nsew", padx=20, pady=(0, 20))
        
    def set_progression_bar_grid(self):
        self.treatment_button.grid(column=1, row=0, sticky="w", pady=20, padx=5)
        self.doctor_button.grid(column=2, row=0, sticky="w", pady=20, padx=5)
        self.appointment_button.grid(column=3, row=0, sticky="w", pady=20, padx=5)
        self.finished_button.grid(column=4, row=0, sticky="w", pady=20, padx=5)
        
    def reset_progression_bar(self):
        self.treatment_button.configure(border_color="red")
        self.doctor_button.configure(text_color=("gray5", "gray95"), fg_color=("gray75", "gray25"), hover_color=("gray75", "gray25"))
        self.appointment_button.configure(text_color=("gray5", "gray95"), fg_color=("gray75", "gray25"), hover_color=("gray75", "gray25"))
        self.finished_button.configure(text_color=("gray5", "gray95"), fg_color=("gray75", "gray25"), hover_color=("gray75", "gray25"))
