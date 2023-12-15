import customtkinter as ctk

from source.classes.customizeTreatmentFrame import TreatmentFrame
from source.classes.chooseDoctorsFrame import chooseDoctorsFrame

class MainBookingFrame(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk):
        super().__init__(master=master, corner_radius=0, fg_color="transparent")
        
        # variables
        self.disabled_kwargs = {
            "text_color": ("gray5", "gray95"),
            "fg_color": ("gray75", "gray25"),
            "hover_color": ("gray75", "gray25")
        }
        self.current_kwargs = {
            "text_color": ("black", "white"),
            "fg_color": ("#3B8ED0", "#1F6AA5"),
            "hover_color": ("#36719F", "#144870")
        }
        self.enabled_kwargs = {
            "text_color": ("black", "white"),
            "fg_color": ("#3e6787", "#324e63"),
            "hover_color": ("#2e4c63", "#243847")
        }
        self.progression: int = 0
        self.current_state_old: int = 0
        self.current_state: int = 0
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # widgets for progression bar
        self.progression_bar_frame = ctk.CTkFrame(self, corner_radius=14)
        self.progression_bar_frame.columnconfigure((0, 5), weight=1)
        
        self.treatment_button = ctk.CTkButton(self.progression_bar_frame, corner_radius=14, text="Behandlung", command=self.treatment_button_pressed)
        self.doctor_button = ctk.CTkButton(self.progression_bar_frame, corner_radius=14, text="Zahnarzt", command=self.doctor_button_pressed)
        self.appointment_button = ctk.CTkButton(self.progression_bar_frame, corner_radius=14, text="Termin", command=self.appointment_button_pressed)
        self.finished_button = ctk.CTkButton(self.progression_bar_frame, corner_radius=14, text="Fertig", command=self.finished_button_pressed)
        
        self.buttons = [self.treatment_button, self.doctor_button, self.appointment_button, self.finished_button]
        
        
        # main frames
        self.main_frames: list[ctk.CTkFrame] = [TreatmentFrame(self), chooseDoctorsFrame(self)]
        self.set_progression_bar_grid()
        self.set_main_grid()
        
        self.reset_progression_bar()
        
    def set_main_grid(self):
        self.progression_bar_frame.grid(column=0, row=0, sticky="new", padx=20, pady=20)
        self.main_frames[0].grid(column=0, row=1, sticky="nsew", padx=20, pady=(0, 20))
        
    def set_progression_bar_grid(self):
        self.treatment_button.grid(column=1, row=0, sticky="w", pady=20, padx=5)
        self.doctor_button.grid(column=2, row=0, sticky="w", pady=20, padx=5)
        self.appointment_button.grid(column=3, row=0, sticky="w", pady=20, padx=5)
        self.finished_button.grid(column=4, row=0, sticky="w", pady=20, padx=5)
        
    def reset_progression_bar(self):
        self.progression = 0
        self.current_state = 0
        self.current_state_old = 0
        self.update_progression_bar()
        
    def update_progression_bar(self):
        
        for index, button in enumerate(self.buttons):
            button.configure(**self.disabled_kwargs)
            if index <= self.progression:
                button.configure(**self.enabled_kwargs)
            if index == self.current_state:
                button.configure(**self.current_kwargs)
        self.main_frames[self.current_state_old].grid_forget()
        self.main_frames[self.current_state].grid(column=0, row=1, sticky="nsew", padx=20, pady=(0, 20))
        self.current_state_old = self.current_state
        print(self.progression, self.current_state, self.current_state_old)
        
    def next_page(self):
        if self.current_state == self.progression:
            self.progression = min(self.progression + 1, 3)
            self.main_frames[self.progression].reset()
            print("reset")
        self.current_state = min(self.current_state + 1, 3)
        self.update_progression_bar()
        
        
    def treatment_button_pressed(self):
        index = 0
        if index <= self.progression:
            self.current_state = index
        self.update_progression_bar()
    
    def doctor_button_pressed(self):
        index = 1
        if index <= self.progression:
            self.current_state = index
        self.update_progression_bar()
    
    def appointment_button_pressed(self):
        index = 2
        if index <= self.progression:
            self.current_state = index
        self.update_progression_bar()
    
    def finished_button_pressed(self):
        index = 3
        if index <= self.progression:
            self.current_state = index
        self.update_progression_bar()
