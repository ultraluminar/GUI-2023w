import customtkinter as ctk

from source.classes.customizeTreatmentFrame import TreatmentFrame
from source.classes.chooseDoctorsFrame import ChooseDoctorsFrame
from source.classes.calenderViewFrame import CalenderViewFrame
from source.classes.finishFrame import FinishFrame

button_configure_kwargs = {
    "disabled": {
            "text_color": ("gray8", "gray92"),
            "fg_color": ("gray75", "gray25"),
            "hover_color": ("gray75", "gray25")},
    "enabled": {
            "text_color": ("black", "white"),
            "fg_color": ("#4f7c9e", "#3a4c5a"),
            "hover_color": ("#456b87", "#2a3741")},
    "current": {
            "text_color": ("black", "white"),
            "fg_color": ("#3B8ED0", "#1F6AA5"),
            "hover_color": ("#36719F", "#144870")}
}

frame_grid_kwargs = {"row": 1, "sticky": "nsew", "padx": 20, "pady": (0, 20), "column": 0}
button_grid_kwargs = {"row": 0, "sticky": "nsew", "padx": 5, "pady": 20}

class MainBookingFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, corner_radius=0, fg_color="transparent")
        
        # variables
        self.data_bundle = {}

        self.progression: int = 0
        self.current_state: int = 0
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # widgets for progression bar
        self.progression_bar_frame = ctk.CTkFrame(self, corner_radius=14)
        self.progression_bar_frame.columnconfigure((0, 5), weight=1)

        button_create_kwargs = [
            {"text": "Behandlung", "command": lambda: self.switch_to(0)},
            {"text": "Zahnarzt", "command": lambda: self.switch_to(1)},
            {"text": "Termin", "command": lambda: self.switch_to(2)},
            {"text": "Fertig", "command": lambda: self.switch_to(3)}
        ]

        self.buttons = [
            ctk.CTkButton(self.progression_bar_frame, corner_radius=14, **kwargs)
            for kwargs in button_create_kwargs]


        # main frames
        self.treatment_frame = TreatmentFrame(self, self.data_bundle)
        self.choose_doctors_frame = ChooseDoctorsFrame(self, self.data_bundle)
        self.calendar_view_frame = CalenderViewFrame(self, self.data_bundle)
        self.finish_frame = FinishFrame(self, self.data_bundle)

        self.main_frames = [self.treatment_frame, self.choose_doctors_frame, self.calendar_view_frame, self.finish_frame]

        self.set_grid()

    def set_grid(self):
        self.progression_bar_frame.grid(column=0, row=0, sticky="new", padx=20, pady=20)
        self.treatment_frame.grid(**frame_grid_kwargs)

        for column, button in enumerate(self.buttons, start=1):
            button.grid(column=column, **button_grid_kwargs)

        
    def reset(self):
        self.progression = -1
        self.current_state = -1
        self.next_page()

        
    def update_progression_bar(self):
        # visual update buttons
        for index, button in enumerate(self.buttons):
            state = "current" if index == self.current_state else "enabled" if index <= self.progression else "disabled"
            button.configure(**button_configure_kwargs[state])

        # show calendar for chosen doctor
        if self.current_state == 2:
            self.calendar_view_frame.update_current()

        # ungrid frame
        for index, frame in enumerate(self.main_frames):
            frame.grid_forget() if index != self.current_state else frame.grid(**frame_grid_kwargs)

        
    def next_page(self):
        if self.current_state == 3:
            return
        if self.current_state == self.progression:
            self.progression += 1
            self.main_frames[self.progression].reset()

        self.current_state += 1
        self.update_progression_bar()

    def switch_to(self, new_state: int):
        if self.current_state != new_state and self.progression >= new_state:
            self.current_state = new_state
            self.update_progression_bar()

        
    def changed(self):
        self.progression = self.current_state
        self.update_progression_bar()
