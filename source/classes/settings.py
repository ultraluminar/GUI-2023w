import customtkinter as ctk

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x400")

        self.label = ctk.CTkLabel(self, text="Settings")
        self.label.pack(padx=20, pady=20)