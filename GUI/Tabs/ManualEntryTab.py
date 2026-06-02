import customtkinter as ctk
import pandas as pd

from GUI.gui_config import HEADER1, HEADER2
from GUI.gui_helper_functions import create_label_entry_pair


class ManualEntryTab:

    def __init__(self, parent, db_conn):
        """Sets up all elements within the 'Manual Entry' tab.
        """
        self.db_conn = db_conn
        
        ctk.CTkLabel(parent, text="Manual Race Entry", font=HEADER1).pack(padx=10, pady=10)

        manual_entry_frame = ctk.CTkFrame(parent, border_width=2)
        manual_entry_frame.pack(padx=10, pady=10)

        race_frame = ctk.CTkFrame(manual_entry_frame)
        self.race_entry = create_label_entry_pair(race_frame, "Race:", values=[""])
        race_frame.pack(padx=10, pady=10)

        runner_frame = ctk.CTkFrame(manual_entry_frame)
        self.runner_entry = create_label_entry_pair(runner_frame, "Runner:", values=[""])
        runner_frame.pack(padx=10, pady=10)

        runner_time_frame = ctk.CTkFrame(manual_entry_frame)
        self.runner_time_entry = create_label_entry_pair(runner_time_frame, "Runner Time:", placeholder_text="hh.mm.ss")
        runner_time_frame.pack(padx=10, pady=10)

        ctk.CTkButton(parent, text="Enter result", command=self.submit_clicked, font=HEADER2).pack(padx=10, pady=10)


    def on_focus(self):
        all_races = []
        for name, distance, date, fixed_points in pd.read_sql("""SELECT name, distance, date, fixed_points FROM races""", self.db_conn).to_numpy():
            if distance is None: distance = ""
            if fixed_points is None: fixed_points = ""
            all_races.append(f"{name} {distance}, {date}, {fixed_points}")
        self.race_entry.configure(values=all_races)

    def submit_clicked(self):
        race = self.race_entry.get()
        runner = self.runner_entry.get()
        runner_time = self.runner_time_entry.get()
        