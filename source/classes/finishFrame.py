import customtkinter as ctk
import tkinter as tk

from source.auth_util import appendCSV, paths

class finishFrame(ctk.CTkFrame):
    def __init__(self, master, bundle: dict):
        super().__init__(master=master)
        
        # variables
        self.data_bundle = bundle
        self.auth_service = self.nametowidget(".").auth_service
        
        # fonts
        self.font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        
        # main widgets
        self.grid_columnconfigure([0, 1, 2], weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.main_heading_label = ctk.CTkLabel(self, text="Buchung bestätigen", font=self.font24)
        self.sub_heading_label = ctk.CTkLabel(self, text="Bestätigen Sie ihre angegebenen Daten und buchen sie verbindlich ihren Termin.")
        self.data_frame = ctk.CTkFrame(self)
        self.confirm_button = ctk.CTkButton(self, text="Verbindlich buchen", command=self.confirm)

        # data subframe widgets
        self.tooth_number_label = ctk.CTkLabel(self.data_frame, text="Anzahl der zu behandelnden Zähne:", anchor="w", width=200)
        self.tooth_number_value_label = ctk.CTkLabel(self.data_frame, width=150, anchor="w")
        self.dental_problem_label = ctk.CTkLabel(self.data_frame, text="Ihr Zahnproblem:", anchor="w", width=200)
        self.dental_problem_value_label = ctk.CTkLabel(self.data_frame, width=150, anchor="w")
        self.doctor_name_label = ctk.CTkLabel(self.data_frame, text="Ihr behandelnder Arzt:", anchor="w", width=200)
        self.doctor_name_value_label = ctk.CTkLabel(self.data_frame, width=150, anchor="w")
        self.date_label = ctk.CTkLabel(self.data_frame, text="Ihr Termin:", anchor="w", width=200)
        self.date_value_label = ctk.CTkLabel(self.data_frame, width=150, anchor="w")
        self.total_cost_label = ctk.CTkLabel(self.data_frame, text="Ihre Gesamtkosten:", anchor="w", width=200)
        self.total_cost_value_label = ctk.CTkLabel(self.data_frame, width=150, anchor="w")
        
        self.set_data_frame_grid()
        self.set_main_grid()
        
        
    def set_main_grid(self):
        self.main_heading_label.grid(column=1, row=0, pady=(20, 0), sticky="nsew")
        self.sub_heading_label.grid(column=1, row=1, sticky="nsew")
        self.data_frame.grid(column=1, row=2, pady=20, sticky="nsew")
        self.confirm_button.grid(column=1, row=3, pady=(0, 20), sticky="e", padx=(0, 20))
    
    def set_data_frame_grid(self):
        self.tooth_number_label.grid(column=0, row=0, pady=(10, 0), padx=(20, 0))
        self.tooth_number_value_label.grid(column=1, row=0, pady=(10, 0), padx=(0, 20))
        self.dental_problem_label.grid(column=0, row=1, pady=(10, 0), padx=(20, 0))
        self.dental_problem_value_label.grid(column=1, row=1, pady=(10, 0), padx=(0, 20))
        self.doctor_name_label.grid(column=0, row=2, pady=(10, 0), padx=(20, 0))
        self.doctor_name_value_label.grid(column=1, row=2, pady=(10, 0), padx=(0, 20))
        self.date_label.grid(column=0, row=3, pady=(10, 0), padx=(20, 0))
        self.date_value_label.grid(column=1, row=3, pady=(10, 0), padx=(0, 20))
        self.total_cost_label.grid(column=0, row=4, pady=(10, 0), padx=(20, 0))
        self.total_cost_value_label.grid(column=1, row=4, pady=(10, 0), padx=(0, 20))
            
    def data_frame_ungrid(self):
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
        self.data_frame_ungrid()
        username = self.auth_service.username
        #TODO: change variable names to actual names in bundle
        self.tooth_number_value_label.configure(text=self.data_bundle["tooth_number"])
        self.dental_problem_value_label.configure(text=self.data_bundle["dental_problem"])
        self.doctor_name_value_label.configure(text=self.data_bundle["doctor"])
        self.date_value_label.configure(text=self.data_bundle["date"])
        self.total_cost_value_label.configure(text=self.data_bundle["total_cost"])
            
        self.set_doctors_grid()
        self.set_main_grid()
        
    def confirm(self):
        appendCSV(paths["appointments"], self.data_bundle["appointment_row"])
        self.master.next_page()
        