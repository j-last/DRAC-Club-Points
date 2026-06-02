import customtkinter as ctk

from config import HEADER1, HEADER2
from helper_functions import create_label_entry_pair


class ManualEntryTab:

    def __init__(self, parent):
        """Sets up all elements within the 'Manual Entry' tab.
        """
        
        ctk.CTkLabel(parent, text="Manual Race Entry", font=HEADER1).pack(padx=10, pady=10)

        manual_entry_frame = ctk.CTkFrame(parent, border_width=2)
        manual_entry_frame.pack(padx=10, pady=10)

        race_frame = ctk.CTkFrame(manual_entry_frame)
        self.race_entry = create_label_entry_pair(race_frame, "Race:", values=["Random Race 5k"]*10)
        race_frame.pack(padx=10, pady=10)

        runner_frame = ctk.CTkFrame(manual_entry_frame)
        self.runner_entry = create_label_entry_pair(runner_frame, "Runner:", values=["Jim Bob"]*10)
        runner_frame.pack(padx=10, pady=10)

        runner_time_frame = ctk.CTkFrame(manual_entry_frame)
        self.runner_time_entry = create_label_entry_pair(runner_time_frame, "Runner Time:", placeholder_text="hh.mm.ss")
        runner_time_frame.pack(padx=10, pady=10)

        ctk.CTkButton(parent, text="Enter result", command=self.submit_clicked, font=HEADER2).pack(padx=10, pady=10)


    def submit_clicked(self):
        race = self.race_entry.get()
        runner = self.runner_entry.get()
        runner_time = self.runner_time_entry.get()
        