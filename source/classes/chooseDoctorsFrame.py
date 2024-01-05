import customtkinter as ctk
import tkinter as tk

from pandas import read_csv

class ChooseDoctorsFrame(ctk.CTkFrame):
    """
    A custom frame for selecting a doctor from a list of available doctors.

    Methods:
        set_main_grid(self):
            Sets the grid layout for the main widgets.
        set_doctors_grid(self):
            Sets the grid layout for the doctor select frames.
        doctors_ungrid(self):
            Removes the doctor select frames and radio buttons from the grid layout.
        reset(self):
            Resets the frame by updating the list of available doctors and refreshing the grid layout.
        next_page(self):
            Stores the chosen doctor's username in the data bundle and proceeds to the next page.
        get_doctor(self):
            Placeholder function. Returns the chosen doctor.
    """
    def __init__(self, master, bundle: dict):
        """
        Initializes the ChooseDoctorsFrame.

        Args:
            master: The parent widget.
            bundle (dict): A dictionary to store data.
        """
        super().__init__(master=master)
        
        # variables
        self.doctor_csv_path = "data/doctors.csv"
        self.patients_csv_path = "data/patients.csv"
        self.df_doctors = None
        self.df_patients = None
        self.doctor_list: list[tuple] = []
        self.data_bundle = bundle
        
        # fonts
        self.font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        
        # main widgets
        self.grid_columnconfigure([0, 1, 2, 4, 5, 6], weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.main_heading_label = ctk.CTkLabel(self, text="Zahnarzt auswählen", font=self.font24)
        self.sub_heading_label = ctk.CTkLabel(self, text="Von welchem unserer Ärzte wollen sie behandelt werden?")
        self.next_button = ctk.CTkButton(self, text="Weiter", command=self.next_page)

        # doctors sub Frame
        self.var_chosen_doctor_username = tk.StringVar()
        self.doctor_list_frame = ctk.CTkScrollableFrame(self)
        self.doctor_list_frame.grid_columnconfigure((0, 2), weight=1)
        self.doctor_select_frames: list[ctk.CTkFrame] = []
        self.doctor_select_radio: list[ctk.CTkRadioButton] = []
        
        self.set_doctors_grid()
        self.set_main_grid()
        
        
    def set_main_grid(self):
        """
        Sets the grid layout for the main widgets.
        """
        self.main_heading_label.grid(column=3, row=0, pady=(20, 0), sticky="nsew")
        self.sub_heading_label.grid(column=3, row=1, sticky="nsew")
        self.doctor_list_frame.grid(column=1, columnspan=5, row=2, pady=20, sticky="nsew")
        self.next_button.grid(column=0, columnspan=7, row=3, pady=20, sticky="e", padx=(0, 20))
    
    def set_doctors_grid(self):
        """
        Sets the grid layout for the doctor select frames.
        """
        for radio in self.doctor_select_radio:
            radio.grid(column=0, row=0, sticky="nsew", padx=15, pady=15)
        for index, frame in enumerate(self.doctor_select_frames):
            frame.grid(column=1, row=index, sticky="nsew", pady=(15, 0))
            
    def doctors_ungrid(self):
        """
        Removes the doctor select frames and radio buttons from the grid layout.
        """
        for radio in self.doctor_select_radio:
            radio.grid_forget()
        for frame in self.doctor_select_frames:
            frame.grid_forget()            

    def reset(self):
        """
        Resets the frame by updating the list of available doctors and refreshing the grid layout.
        """
        self.df_doctors = read_csv(self.doctor_csv_path)
        self.df_patients = read_csv(self.patients_csv_path)
        self.doctors_ungrid()
        patient_insurance_type = self.df_patients.loc[self.df_patients["Username"] == self.data_bundle["username"], "Krankenkassenart"].iloc[0]
        
        # find available doctors
        df_available_doctors = self.df_doctors.loc[self.df_doctors[patient_insurance_type] == True, ["Username", "Name"]]   
        self.doctor_list = [tuple(x) for x in df_available_doctors.to_records(index=False)]  # convert to list of tuples(Username, Name)
        self.var_chosen_doctor_username.set(self.doctor_list[0][0])  # prechoose the first doctor in list
        
        # fill doctor select frames
        self.doctor_select_frames = [ctk.CTkFrame(self.doctor_list_frame) for _ in range(0, len(self.doctor_list))]  # create frames
        # create radio buttons
        for index, frame in enumerate(self.doctor_select_frames): 
            self.doctor_select_radio.append(ctk.CTkRadioButton(frame, text=self.doctor_list[index][1], variable=self.var_chosen_doctor_username, value=self.doctor_list[index][0], command=self.master.changed))
            
        self.set_doctors_grid()
        self.set_main_grid()
        
    def next_page(self, *args):
        """
        Stores the chosen doctor's username in the data bundle and proceeds to the next page.
        """
        self.data_bundle["doctor"] = self.var_chosen_doctor_username.get()
        self.master.next_page()
        