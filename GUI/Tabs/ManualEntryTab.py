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


    def on_focus(self):
        all_races = []
        for name, distance, date in pd.read_sql("""SELECT name, distance, date FROM races""", self.db_conn).to_numpy():
            if distance is None: distance = ""
            all_races.append(f"{name} {distance} ({date})")
        self.race_entry.configure(values=all_races)

        all_runners = []
        for firstname, lastname in pd.read_sql("""SELECT firstname, lastname FROM runners""", self.db_conn).to_numpy():
            all_runners.append(f"{firstname} {lastname}")
        self.runner_entry.configure(values = all_runners)

    def submit_clicked(self):
        race_name = self.race_entry.get().strip().split()[0]
        firstname, lastname = self.runner_entry.get().strip().split()
        runner_time = self.runner_time_entry.get()

        # Input validation not yet implemented
        # Also need to convert to a time object

        runner_id = pd.read_sql(f"""SELECT runner_id 
                                FROM runners 
                                WHERE firstname='{firstname}' AND lastname='{lastname}'
                                """, self.db_conn).to_numpy()[0][0]
        
        race_id = pd.read_sql(f"""SELECT race_id 
                                FROM races 
                                WHERE name='{race_name}'
                                """, self.db_conn).to_numpy()[0][0]

        RaceResultsTable.add_entry(self.db_conn, int(runner_id), int(race_id), runner_time)
        