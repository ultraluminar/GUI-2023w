import customtkinter as ctk

from source.classes.customizeTreatmentFrame import TreatmentFrame
from source.classes.chooseDoctorsFrame import ChooseDoctorsFrame
from source.classes.calenderViewFrame import CalenderViewFrame
from source.classes.finishFrame import FinishFrame
from source.auth_util import getfromCSV, paths

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
    """
    The main booking frame that displays the booking process.

    Args:
        master: The parent widget.
        bundle (dict): A dictionary containing data bundle.

    Methods:
        set_progress_bar_grid(): Sets the grid layout for the progression bar.
        set_no_teeth_grid(): Sets the grid layout for the no_teeth_frame.
        reset(): Resets the booking process.
        update_progression_bar(): Updates the progression bar and frame visibility based on the current state.
        next_page(): Goes to the next page in the booking process.
        ungrid_all(): Hides all frames.
        switch_to(new_state: int): Switches to the specified page in the booking process (progressbar).
        changed(): Called when data is changed on some page.
    """

    def __init__(self, master, bundle: dict):
        """
        Initialize the MainBookingFrame.

        Args:
            master: The parent widget.
            bundle (dict): A dictionary containing data bundle.
        """
        super().__init__(master=master, corner_radius=0, fg_color="transparent")
        
        # variables
        self.data_bundle = bundle
        self.main_sidebar = self.nametowidget(".").main_sidebar   # get login sidebar from app

        self.progression: int = 0
        self.current_state: int = 0
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # fonts
        self.font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")

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

        # list of main frames
        self.main_frames: list[ctk.CTkFrame] = [self.treatment_frame, self.choose_doctors_frame, self.calendar_view_frame, self.finish_frame]

        # widgets for frame when patient has no teeth to treat
        self.no_teeth_frame = ctk.CTkFrame(self)
        self.no_teeth_frame.columnconfigure((0, 2), weight=1)
        self.no_teeth_heading_label = ctk.CTkLabel(self.no_teeth_frame, text="Keine Behandlung möglich", font=self.font24)
        explainer_text = """Es scheint, dass Sie keine Zähne haben, die einer Behandlung bedürfen.
        
        Dies kann verschiedene Gründe haben, wie zum Beispiel eine bereits
        abgeschlossene Behandlung, eine fehlende Zahnproblematik oder bereits gebuchte Termine.
        
        Falls Sie dennoch Fragen oder Bedenken haben, empfehlen wir Ihnen,
        sich an Ihren Zahnarzt zu wenden, um weitere Informationen zu erhalten.
        
        Vielen Dank für Ihr Verständnis."""
        self.no_teeth_label = ctk.CTkLabel(self.no_teeth_frame, text=explainer_text)
        self.no_teeth_button = ctk.CTkButton(self.no_teeth_frame, text="Zurück zur Startseite", command=self.main_sidebar.home)


    def set_progress_bar_grid(self):
        """
        Set the grid for the progression bar frame and treatment frame.
        """
        self.progression_bar_frame.grid(column=0, row=0, sticky="new", padx=20, pady=20)
        self.treatment_frame.grid(**frame_grid_kwargs)

        for column, button in enumerate(self.buttons, start=1):
            button.grid(column=column, **button_grid_kwargs)

    def set_no_teeth_grid(self):
        """
        Set the grid for the no_teeth_frame.
        """
        self.no_teeth_frame.grid(column=0, row=0, sticky="new", padx=20, pady=20)
        self.no_teeth_heading_label.grid(column=1, row=0, sticky="nsew", pady=(20, 0))
        self.no_teeth_label.grid(column=1, row=1, sticky="nsew", pady=(20, 0))
        self.no_teeth_button.grid(column=1, row=2, sticky="nsew", pady=(20, 20))
        
    def reset(self):
        """
        Reset the booking process.

        If the patient has no teeth to treat, show the no_teeth_frame.
        Otherwise, reset the progression, show the progression bar, and show the first frame.
        """
        self.ungrid_all()   # hide all frames
        # check if patient has teeth to treat
        if int(getfromCSV(paths["patients"]["csv"], ("Username", self.data_bundle["username"]), "Anzahl zu behandelnder Zähne")) < 1:
            # if not, show no_teeth_frame only
            self.set_no_teeth_grid()
            return
        # if yes, reset progression, show progression bar and show first frame
        self.progression = -1
        self.current_state = -1
        self.set_progress_bar_grid()
        self.next_page()

        
    def update_progression_bar(self):
        """
        Update the progression bar and frame visibility based on the current state.
        """
        # visual update buttons
        for index, button in enumerate(self.buttons):
            state = "current" if index == self.current_state else "enabled" if index <= self.progression else "disabled"
            button.configure(**button_configure_kwargs[state])


        # ungrid frame
        for index, frame in enumerate(self.main_frames):
            frame.grid_forget() if index != self.current_state else frame.grid(**frame_grid_kwargs)

        
    def next_page(self):
        """
        Go to the next page in the booking process.

        If it is the last page, do nothing.
        If the current state is equal to the progression, increment the progression and reset the current frame.
        Increment the current state and update the progression bar.
        """
        if self.current_state == 3:    # if last page,
            return
        if self.current_state == self.progression:  
            self.progression += 1
            self.main_frames[self.progression].reset()

        self.current_state += 1
        self.update_progression_bar()

    def ungrid_all(self):
        """
        Hide all frames.
        """
        self.progression_bar_frame.grid_forget()
        self.no_teeth_frame.grid_forget()
        for frame in self.main_frames:
            frame.grid_forget()

    def switch_to(self, new_state: int):
        """
        Switch to the specified page in the booking process (progressbar).

        Args:
            new_state (int): The index of the new state.

        Notes:
            This method is called when a button in the progression bar is clicked.
            It only switches to a page if the new state is less than or equal to the current progression.
        """
        if self.current_state != new_state and self.progression >= new_state:
            self.current_state = new_state
            self.update_progression_bar()
        
    def changed(self):
        """
        Called when data is changed on some page.

        Resets the progression to the current state and updates the progression bar.
        """
        self.progression = self.current_state   # resets progression to current state
        self.update_progression_bar()
