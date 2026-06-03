import customtkinter as ctk
import pandas as pd

from GUI.gui_config import HEADER1, HEADER2
from GUI.gui_helper_functions import create_label_entry_pair

from Database.RaceResultsTable import RaceResultsTable


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

        self.on_focus()


    def on_focus(self):
        self.all_races = {}
        for race_id, name, distance, date in pd.read_sql("""SELECT race_id, name, distance, date FROM races""", self.db_conn).to_numpy():
            if distance is None: distance = ""
            self.all_races[f"{name} {distance} ({date})"] = race_id
        self.race_entry.configure(values=self.all_races.keys())

        self.all_runners = {}
        for runner_id, firstname, lastname in pd.read_sql("""SELECT runner_id, firstname, lastname FROM runners""", self.db_conn).to_numpy():
            self.all_runners[f"{firstname} {lastname}"] = runner_id
        self.runner_entry.configure(values=self.all_runners.keys())

    def submit_clicked(self):
        race = self.race_entry.get().strip()
        runner = self.runner_entry.get()
        runner_time = self.runner_time_entry.get()

        # Input validation not yet implemented
        # Also need to convert to a time object

        runner_id = self.all_runners[runner]
        race_id = self.all_races[race]

        RaceResultsTable.add_entry(self.db_conn, runner_id, race_id, runner_time)
        