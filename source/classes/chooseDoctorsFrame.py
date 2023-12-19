import customtkinter as ctk
import tkinter as tk

from pandas import read_csv

class chooseDoctorsFrame(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk):
        super().__init__(master=master)
        
        # variables
        self.auth_service = self.nametowidget(".").auth_service
        self.doctor_csv_path = "data/doctors.csv"
        self.patients_csv_path = "data/patients.csv"
        self.df_doctors = read_csv(self.doctor_csv_path)
        self.df_patients = read_csv(self.patients_csv_path)
        self.doctor_list: list[tuple] = []
        
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
        self.main_heading_label.grid(column=3, row=0, pady=(20, 0), sticky="nsew")
        self.sub_heading_label.grid(column=3, row=1, sticky="nsew")
        self.doctor_list_frame.grid(column=1, columnspan=5, row=2, pady=20, sticky="nsew")
        self.next_button.grid(column=0, columnspan=7, row=3, pady=20, sticky="e", padx=(0, 20))
    
    def set_doctors_grid(self):
        for radio in self.doctor_select_radio:
            radio.grid(column=0, row=0, sticky="nsew", padx=15, pady=15)
        for index, frame in enumerate(self.doctor_select_frames):
            frame.grid(column=1, row=index, sticky="nsew", pady=(15, 0))
            
    def doctors_ungrid(self):
        for radio in self.doctor_select_radio:
            radio.grid_forget()
        for frame in self.doctor_select_frames:
            frame.grid_forget()            

    def reset(self):
        self.doctors_ungrid()
        username = self.auth_service.username
        print(username)
        patient_insurance_type = self.df_patients.loc[self.df_patients["Username"] == username, "Krankenkassenart"].iloc[0]
        
        # find available doctors
        df_available_doctors = self.df_doctors.loc[self.df_doctors[patient_insurance_type] == True, ["Username", "Name"]]   
        self.doctor_list = [tuple(x) for x in df_available_doctors.to_records(index=False)] # convert to list of tuples(Username, Name)
        self.var_chosen_doctor_username.set(self.doctor_list[0][0])  # prechoose the first doctor in list
        
        # fill doctor select frames
        self.doctor_select_frames = [ctk.CTkFrame(self.doctor_list_frame) for i in range(0, len(self.doctor_list))] # create frames 
        # create radio buttons
        for index, frame in enumerate(self.doctor_select_frames): 
            self.doctor_select_radio.append(ctk.CTkRadioButton(frame, text=self.doctor_list[index][1], variable=self.var_chosen_doctor_username, value=self.doctor_list[index][0], command=self.master.changed))
            
        self.set_doctors_grid()
        self.set_main_grid()
        
    def next_page(self):
        self.master.next_page()
        
    def get_doctor(self):
        return self.var_chosen_doctor_username.get()
        