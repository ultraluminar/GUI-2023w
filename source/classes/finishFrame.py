import customtkinter as ctk

from datetime import datetime
from CTkToolTip import CTkToolTip
import logging

from source.auth_util import getfromCSV, updateCSV, appendCSV, paths

class FinishFrame(ctk.CTkFrame):
    """
    A class representing the finish frame of a booking confirmation GUI.

    Methods:
        __init__(self, master, bundle: dict):
            Initializes a new instance of the FinishFrame class.
        set_main_grid(self):
            Sets the grid layout for the main widgets in the finish frame.
        set_data_frame_grid(self):
            Sets the grid layout for the data subframe widgets in the finish frame.
        data_frame_ungrid(self):
            Removes the data subframe widgets from the grid layout.
        reset(self):
            Resets the finish frame by updating the data labels and re-setting the grid layout.
        confirm(self):
            Confirms the booking by updating the tooth count, adding the appointment to the CSV file, and logging the booking.
    """
    def __init__(self, master, bundle: dict):
        """
        Initializes a new instance of the FinishFrame class.

        Args:
            master: The parent widget.
            bundle (dict): A dictionary containing the booking data.
        """
        super().__init__(master=master)
        
        # variables
        self.data_bundle = bundle
        self.main_sidebar = self.nametowidget(".").main_sidebar
        
        # fonts
        self.font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        self.fat = ctk.CTkFont(family="Segoe UI", weight="bold")
        
        # main widgets
        self.grid_columnconfigure((0, 2), weight=1)
        self.main_heading_label = ctk.CTkLabel(self, text="Buchung bestätigen", font=self.font24)
        self.sub_heading_label = ctk.CTkLabel(self, text="Bestätigen Sie ihre angegebenen Daten und buchen sie verbindlich ihren Termin.")
        self.data_frame = ctk.CTkFrame(self)
        self.confirm_button = ctk.CTkButton(self, text="Verbindlich buchen", command=self.next_page)

        # data subframe widgets
        self.tooth_number_label = ctk.CTkLabel(self.data_frame, text="Anzahl der zu behandelnden Zähne:", anchor="w", width=250)
        self.tooth_number_value_label = ctk.CTkLabel(self.data_frame, width=200, anchor="w", font=self.fat)
        self.dental_problem_label = ctk.CTkLabel(self.data_frame, text="Ihr Zahnproblem:", anchor="w", width=250)
        self.dental_problem_value_label = ctk.CTkLabel(self.data_frame, width=200, anchor="w", font=self.fat)
        self.doctor_name_label = ctk.CTkLabel(self.data_frame, text="Ihr behandelnder Arzt:", anchor="w", width=250)
        self.doctor_name_value_label = ctk.CTkLabel(self.data_frame, width=200, anchor="w", font=self.fat)
        self.date_label = ctk.CTkLabel(self.data_frame, text="Ihr Termin:", anchor="w", width=250)
        self.date_value_label = ctk.CTkLabel(self.data_frame, width=200, anchor="w", font=self.fat)
        self.total_cost_label = ctk.CTkLabel(self.data_frame, text="Ihre Gesamtkosten:", anchor="w", width=250)
        self.total_cost_value_label = ctk.CTkLabel(self.data_frame, width=200, anchor="w", font=self.fat)
        
        # tooltips
        CTkToolTip(self.confirm_button, "Klicken um den Termin verbindlich zu buchen. (Enter)", alpha=0.8)
        
        self.set_data_frame_grid()
        self.set_main_grid()
        
        
    def set_main_grid(self):
        """
        Sets the grid layout for the main widgets in the finish frame.
        """
        self.main_heading_label.grid(column=1, row=0, pady=(20, 0), sticky="nsew")
        self.sub_heading_label.grid(column=1, row=1, sticky="nsew")
        self.data_frame.grid(column=1, row=2, pady=20, sticky="nsew")
        self.confirm_button.grid(column=1, row=3, pady=(0, 20), sticky="e")
    
    def set_data_frame_grid(self):
        """
        Sets the grid layout for the data subframe widgets in the finish frame.
        """
        self.tooth_number_label.grid(column=0, row=0, pady=(20, 0), padx=(20, 0), sticky="nsew")
        self.tooth_number_value_label.grid(column=1, row=0, pady=(20, 0), padx=(0, 20), sticky="nsew")
        self.dental_problem_label.grid(column=0, row=1, pady=(10, 0), padx=(20, 0), sticky="nsew")
        self.dental_problem_value_label.grid(column=1, row=1, pady=(10, 0), padx=(0, 20), sticky="nsew")
        self.doctor_name_label.grid(column=0, row=2, pady=(10, 0), padx=(20, 0), sticky="nsew")
        self.doctor_name_value_label.grid(column=1, row=2, pady=(10, 0), padx=(0, 20), sticky="nsew")
        self.date_label.grid(column=0, row=3, pady=(10, 0), padx=(20, 0), sticky="nsew")
        self.date_value_label.grid(column=1, row=3, pady=(10, 0), padx=(0, 20), sticky="nsew")
        self.total_cost_label.grid(column=0, row=4, pady=(10, 20), padx=(20, 0), sticky="nsew")
        self.total_cost_value_label.grid(column=1, row=4, pady=(10, 20), padx=(0, 20), sticky="nsew")
            
    def data_frame_ungrid(self):
        """
        Removes the data subframe widgets from the grid layout.
        """
        self.tooth_number_label.grid_forget()
        self.tooth_number_value_label.grid_forget()
        self.dental_problem_label.grid_forget()
        self.dental_problem_value_label.grid_forget()
        self.doctor_name_label.grid_forget()
        self.doctor_name_value_label.grid_forget()
        self.date_label.grid_forget()
        self.date_value_label.grid_forget()
        self.total_cost_label.grid_forget()
        self.total_cost_value_label.grid_forget()

    def reset(self):
        """
        Resets the finish frame by updating the data labels and re-setting the grid layout.
        """
        self.data_frame_ungrid()
        self.tooth_number_value_label.configure(text=self.data_bundle["tooth_count"])
        self.dental_problem_value_label.configure(text=self.data_bundle["dental_problem"])
        self.doctor_name_value_label.configure(text=self.data_bundle["doctor"])
        self.date_value_label.configure(text=datetime.strptime(self.data_bundle["dt_start"], "%d-%m-%Y %H:%M").strftime("am %d.%m.%y um %H:%M Uhr"))
        self.total_cost_value_label.configure(text=self.data_bundle["total_cost"])
        
        self.set_data_frame_grid()
        self.set_main_grid()
        
    def next_page(self, *args):
        """
        Sets the grid layout for the data subframe widgets in the finish frame.
        """
        new_tooth_count = getfromCSV(paths["patients"]["csv"], ("Username", self.data_bundle["username"]), "Anzahl zu behandelnder Zähne")
        new_tooth_count -= self.data_bundle["tooth_count"]

        updateCSV(paths["patients"]["csv"], ("Username", self.data_bundle["username"]), ("Anzahl zu behandelnder Zähne", new_tooth_count))

        appendCSV(paths["appointments"], self.data_bundle["appointment_row"])
        logging.info(f"Appointment booked: {self.data_bundle['appointment_row']}")

        self.main_sidebar.home()
        self.nametowidget(".!ctkframe3.!canvas.!homeframe").displayAppointmentFeedback()
