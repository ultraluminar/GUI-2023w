import customtkinter as ctk
import tkinter as tk

from pandas import read_csv

class TreatmentFrame(ctk.CTkFrame):
    def __init__(self, master, bundle: dict):
        super().__init__(master=master)
        
        # variables
        self.auth_service = self.nametowidget(".").auth_service
        self.username = None
        self.cost = None
        self.total_teeth_count = None
        self.dental_problem = None
        self.insurance_shares = None
        self.data_bundle = bundle

        self.fillings = ["normal", "hochwertig", "höchstwertig"]
        
        # fonts
        self.font24 = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        self.font20 = ctk.CTkFont(family="Segoe UI", size=20, weight="bold")
        self.fat = ctk.CTkFont(weight="bold")

        # main widgets
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.main_heading_label = ctk.CTkLabel(self, text="Behandlung anpassen", font=self.font24)
        self.sub_heading_label = ctk.CTkLabel(self, text="Passen sie ihre nächste Behandlung auf ihre Wünsche an!")
        self.next_button = ctk.CTkButton(self, text="Weiter", command=self.next_page)

        # teeth selector subframe
        # variables
        self.teeth_count = tk.IntVar(value=1)
        self.teeth_count_string = tk.StringVar(value="1")
        # widgets
        self.teeth_selector_frame = ctk.CTkFrame(self)
        self.teeth_selector_frame.grid_columnconfigure((0, 2), weight=1)
        self.teeth_selector_heading_label = ctk.CTkLabel(self.teeth_selector_frame, text="Zähne", font=self.font20)
        self.teeth_selector_sub_heading_label = ctk.CTkLabel(self.teeth_selector_frame, text="Wählen sie aus, wie viele Zähne sie bei ihrem nächsten Termin\nbehandeln lassen wollen.")
        self.slider_sub_frame = ctk.CTkFrame(self.teeth_selector_frame)
        self.slider_sub_frame.grid_columnconfigure((0, 4), weight=1)
        self.teeth_selector_counter_label = ctk.CTkLabel(self.slider_sub_frame, textvariable=self.teeth_count_string)
        self.teeth_selector_from_label = ctk.CTkLabel(self.slider_sub_frame, text="1")
        self.teeth_selector_slider = ctk.CTkSlider(self.slider_sub_frame, from_=0, to=2, number_of_steps=2, variable=self.teeth_count, command=self.update_teeth_count)
        self.teeth_selector_to_label = ctk.CTkLabel(self.slider_sub_frame, text="2")
        
        # filling selector subframe
        # variables
        self.filling = tk.StringVar(value="normal")
        # widgets
        self.filling_selector_frame = ctk.CTkFrame(self)
        self.filling_selector_frame.grid_columnconfigure((0, 2), weight=1)
        self.filling_selector_heading_label = ctk.CTkLabel(self.filling_selector_frame, text="Füllung", font=self.font20)
        self.filling_selector_sub_heading_label = ctk.CTkLabel(self.filling_selector_frame, text="Wählen sie aus, welches Füllmaterial verwendet werden soll.")
        self.low_filling_radio = ctk.CTkRadioButton(self.filling_selector_frame, text="an error occured", variable=self.filling, value="normal", command=self.update_bill)
        self.mid_filling_radio = ctk.CTkRadioButton(self.filling_selector_frame, text="an error occured", variable=self.filling, value="hochwertig", command=self.update_bill)
        self.high_filling_radio = ctk.CTkRadioButton(self.filling_selector_frame, text="an error occured", variable=self.filling, value="höchstwertig", command=self.update_bill)
        
        # billing subframe
        # variables
        cell_width = 200
        # widgets
        self.bill_frame = ctk.CTkScrollableFrame(self)
        self.bill_frame.grid_columnconfigure((0, 2), weight=1)
        self.bill_heading_label = ctk.CTkLabel(self.bill_frame, text="Preis", font=self.font20)
        self.bill_sub_heading_label = ctk.CTkLabel(self.bill_frame, text="Hier können sie ihre Rechnung sehen.")
        
        self.bill_sub_frame = ctk.CTkFrame(self.bill_frame)
        self.head_row_description_label = ctk.CTkLabel(self.bill_sub_frame, width=cell_width, font=self.fat, text="Beschreibung")
        self.head_row_single_cost_label = ctk.CTkLabel(self.bill_sub_frame, width=cell_width, font=self.fat, text="Einzelpreis")
        self.head_row_count_label = ctk.CTkLabel(self.bill_sub_frame, width=cell_width, font=self.fat, text="Menge")
        self.head_row_cost_label = ctk.CTkLabel(self.bill_sub_frame, width=cell_width, font=self.fat, text="Betrag")

        self.description_label = ctk.CTkLabel(self.bill_sub_frame, width=cell_width)
        self.single_cost_label = ctk.CTkLabel(self.bill_sub_frame, width=cell_width)
        self.count_label = ctk.CTkLabel(self.bill_sub_frame, width=cell_width)
        self.cost_label = ctk.CTkLabel(self.bill_sub_frame, width=cell_width, font=self.fat)
        
        self.first_line = ctk.CTkFrame(self.bill_sub_frame, height=3, fg_color="gray50")
        
        self.step_sum_label = ctk.CTkLabel(self.bill_sub_frame, width=cell_width, text="Zwischensumme")
        self.step_sum_value_label = ctk.CTkLabel(self.bill_sub_frame, width=cell_width, font=self.fat)

        self.insurance_share_label = ctk.CTkLabel(self.bill_sub_frame, width=cell_width)
        self.insurance_share_value_label = ctk.CTkLabel(self.bill_sub_frame, width=cell_width, font=self.fat)

        self.second_line = ctk.CTkFrame(self.bill_sub_frame, height=3, fg_color="gray50")

        self.total_cost_label = ctk.CTkLabel(self.bill_sub_frame, width=cell_width, text="Gesamtsumme")
        self.total_cost_value_label = ctk.CTkLabel(self.bill_sub_frame, width=cell_width, font=self.fat, text_color="#00C957")
                
        
        # grid
        self.set_teeth_selector_grid()
        self.set_filling_grid()
        self.set_bill_grid()
        self.set_main_grid()
        
    def set_main_grid(self):
        self.main_heading_label.grid(column=0, row=0, columnspan=2, pady=(20, 0), sticky="new")
        self.sub_heading_label.grid(column=0, row=1, columnspan=2, pady=(0, 20), sticky="new")
        self.teeth_selector_frame.grid(column=0, row=2, padx=(20, 10), sticky="nsew")
        self.filling_selector_frame.grid(column=1, row=2, padx=(0, 20), sticky="nsew")
        self.bill_frame.grid(column=0, row=3, columnspan=2, padx=20, pady=(10, 0), sticky="nsew")
        self.next_button.grid(column=0, columnspan=3, row=4, pady=20, sticky="e", padx=(0, 20))
    
    def set_teeth_selector_grid(self):
        self.teeth_selector_counter_label.grid(column=2, row=0)
        self.teeth_selector_from_label.grid(column=1, row=1)
        self.teeth_selector_slider.grid(column=2, row=1)
        self.teeth_selector_to_label.grid(column=3, row=1)
        
        self.teeth_selector_heading_label.grid(column=1, row=0, pady=(15, 0), sticky="nsew")
        self.teeth_selector_sub_heading_label.grid(column=1, row=1, pady=(0, 15), sticky="nsew")
        self.slider_sub_frame.grid(column=1, row=2, padx=15, pady=(0, 15), sticky="nsew")
    
    def set_filling_grid(self):
        self.filling_selector_heading_label.grid(column=1, row=0, pady=(15, 0), sticky="nsew")
        self.filling_selector_sub_heading_label.grid(column=1, row=1, pady=(0, 15), sticky="nsew")

        self.low_filling_radio.grid(column=1, row=2, padx=20, sticky="nsew")
        self.mid_filling_radio.grid(column=1, row=3, padx=20, pady=5, sticky="nsew")
        self.high_filling_radio.grid(column=1, row=4, padx=20, pady=(0, 20), sticky="nsew")
    
    def set_bill_grid(self):
        self.head_row_description_label.grid(column=1, row=0, pady=(15, 0), padx=(15, 0))
        self.head_row_single_cost_label.grid(column=2, row=0, pady=(15, 0), padx=(5, 0))
        self.head_row_count_label.grid(column=3, row=0, pady=(15, 0), padx=(5, 0))
        self.head_row_cost_label.grid(column=4, row=0, pady=(15, 0), padx=(5, 15))
        
        self.description_label.grid(column=1, row=1, pady=(15,0), padx=(15, 0))
        self.single_cost_label.grid(column=2, row=1, pady=(15,0), padx=(5, 0))
        self.count_label.grid(column=3, row=1, pady=(15,10), padx=(5, 0))
        self.cost_label.grid(column=4, row=1, pady=(15,10), padx=(5, 15))
        
        self.first_line.grid(column=3, row=2, columnspan=2, sticky="nsew", padx=15)

        self.step_sum_label.grid(column=3, row=3, pady=(10, 0), padx=(5, 0))
        self.step_sum_value_label.grid(column=4, row=3, pady=(10, 0), padx=(5, 15))
        
        self.insurance_share_label.grid(column=3, row=4, pady=(10, 10), padx=(5, 0))
        self.insurance_share_value_label.grid(column=4, row=4, pady=(10, 10), padx=(5, 15))

        self.second_line.grid(column=3, row=5, columnspan=2, sticky="nsew", padx=15)
        
        self.total_cost_label.grid(column=3, row=6, pady=(10, 15), padx=(5, 0))
        self.total_cost_value_label.grid(column=4, row=6, pady=(10, 15), padx=(5, 15))
        
        self.bill_heading_label.grid(column=1, row=0, pady=(15, 0), sticky="nsew")
        self.bill_sub_heading_label.grid(column=1, row=1, pady=(0, 15), sticky="nsew")
        self.bill_sub_frame.grid(column=1, row=2, padx=15, pady=(0, 15), sticky="nsew")
        
        
    def update_teeth_count(self, *args):
        self.teeth_count_string.set(str(self.teeth_count.get()))
        self.update_bill()
        
    def reset(self):
        self.username = self.auth_service.username
        
        df_patients = read_csv("data/patients.csv")
        df_costs = read_csv("data/costs.csv")
        self.total_teeth_count = df_patients.loc[df_patients["Username"] == self.username, "Anzahl zu behandelnder Zähne"].iat[0]
        self.dental_problem = df_patients.loc[df_patients["Username"] == self.username, "Dentale Problematik"].iat[0]
        
        # teeth selector frame
        self.teeth_selector_counter_label.configure(text="1")
        self.teeth_selector_slider.set(1)
        self.teeth_count.set(1)
        self.teeth_count_string.set("1")
        self.teeth_selector_to_label.configure(text=self.total_teeth_count)
        if self.total_teeth_count == 1:
            self.teeth_selector_slider.configure(from_=0, to=1, number_of_steps=1, state="disabled")
        else:
            self.teeth_selector_slider.configure(from_=1, to=int(self.total_teeth_count), number_of_steps=int(self.total_teeth_count)-1, state="normal")
        
        # filling frame
        self.filling.set("normal")
        
        self.cost = df_costs.loc[df_costs["Dentale Problematik"] == self.dental_problem, "Kosten(€)"]
        self.cost = list(self.cost.values)
        
        self.low_filling_radio.configure(text=f"normal - {self.cost[0]}€")
        self.mid_filling_radio.configure(text=f"hochwertig - {self.cost[1]}€")
        self.high_filling_radio.configure(text=f"höchstwertig - {self.cost[2]}€")
        
        # billing frame        
        privat = df_patients.loc[df_patients["Username"] == self.username, "Krankenkassenart"].iat[0] == "privat"
        self.insurance_shares = df_costs.loc[df_costs["Dentale Problematik"] == self.dental_problem, "privater Anteil" if privat else "gesetzlicher Anteil"]
        self.insurance_shares = list(self.insurance_shares.values)
        
        self.update_bill()
        
        
        
    def update_bill(self):
        fillings_index = self.fillings.index(self.filling.get())
        self.insurance_share = self.insurance_shares[fillings_index]
        self.insurance_share_label.configure(text=f"Krankenkassenanteil ({round(100*self.insurance_share)}%)")
        
        single_cost = self.cost[fillings_index]
        
        self.description_label.configure(text=self.dental_problem)
        self.single_cost_label.configure(text=f"{single_cost}€")
        self.count_label.configure(text=f"{self.teeth_count.get()}")
        self.cost_label.configure(text=f"{single_cost * self.teeth_count.get()}€")
        
        self.step_sum_value_label.configure(text=f"{single_cost * self.teeth_count.get()}€")
        insurance_share = single_cost * self.teeth_count.get() * self.insurance_share
        self.insurance_share_value_label.configure(text=f"-{round(insurance_share, 2)}€")
        total_cost_value = (single_cost * self.teeth_count.get()) - (single_cost * self.teeth_count.get() * self.insurance_share)
        self.total_cost_value_label.configure(text=f"{round(total_cost_value, 2)}€")
        
    
    def next_page(self):
        self.master.next_page()
        self.data_bundle.update({
            "dental_problem": self.dental_problem,
            "tooth_count": self.teeth_count.get(),
            "fill_type": self.filling.get()
        })
        