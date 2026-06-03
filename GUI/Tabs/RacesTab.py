
import customtkinter as ctk
import pandas as pd
from tkinter import messagebox

from GUI.gui_config import HEADER1, HEADER2, NORMAL

from Database.RunnersTable import RunnersTable

class RacesTab:

    def __init__(self, parent, db_conn):
        """Sets up all elements within the 'View Races' tab
        """
        self.parent = parent
        self.db_conn = db_conn

        entry_frame = ctk.CTkFrame(parent)
        entry_frame.pack(padx=10, pady=10)
        ctk.CTkLabel(entry_frame, text="Select Race:", font=HEADER2).grid(row=0, column=0, padx=10, pady=10)
        self.race_entry = ctk.CTkComboBox(entry_frame, values=[""], font=NORMAL)
        self.race_entry.grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(entry_frame, text="Find Results", font=HEADER2, command=self.load_results).grid(row=0, column=2, padx=10, pady=10)
        
        self.runners_frame = ctk.CTkFrame(parent, border_width=2)
        self.runners_frame.pack(padx=10, pady=10, expand=True, fill="both")

        self.on_focus()


    def on_focus(self):
        self.all_races = {}
        for race_id, name, distance, date in pd.read_sql("""SELECT race_id, name, distance, date FROM races""", self.db_conn).to_numpy():
            if distance is None: distance = ""
            self.all_races[f"{name} {distance} ({date})"] = race_id
        self.race_entry.configure(values=self.all_races.keys())


    def load_results(self):
        
        race = self.race_entry.get()
        race_id = self.all_races[race]

        self.runners_frame.destroy()
        self.runners_frame = ctk.CTkScrollableFrame(self.parent, border_width=2)
        self.runners_frame.pack(padx=10, pady=10, expand=True, fill="both")

        for col in range(5): self.runners_frame.columnconfigure(col, weight=1)

        ctk.CTkLabel(self.runners_frame, text="First name", font=HEADER2).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkLabel(self.runners_frame, text="Last name", font=HEADER2).grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkLabel(self.runners_frame, text="Gender", font=HEADER2).grid(row=0, column=2, padx=10, pady=10)
        ctk.CTkLabel(self.runners_frame, text="Age Category", font=HEADER2).grid(row=0, column=3, padx=10, pady=10)
        ctk.CTkLabel(self.runners_frame, text="Time", font=HEADER2).grid(row=0, column=4, padx=10, pady=10)
        ctk.CTkLabel(self.runners_frame, text="Points", font=HEADER2).grid(row=0, column=5, padx=10, pady=10)

        runners = pd.read_sql(f"""SELECT firstname, lastname, gender, age_category, runner_time
                              FROM runners
                              JOIN race_results ON runners.runner_id = race_results.runner_id
                              WHERE race_results.race_id = {race_id}""", self.db_conn).to_numpy()
        
        row_num = 1
        for firstname, lastname, gender, age_cat, time in runners:
            ctk.CTkLabel(self.runners_frame, text=firstname, font=NORMAL).grid(row=row_num, column=0, padx=10, pady=10)
            ctk.CTkLabel(self.runners_frame, text=lastname, font=NORMAL).grid(row=row_num, column=1, padx=10, pady=10)
            ctk.CTkLabel(self.runners_frame, text=gender, font=NORMAL).grid(row=row_num, column=2, padx=10, pady=10)
            ctk.CTkLabel(self.runners_frame, text=age_cat, font=NORMAL).grid(row=row_num, column=3, padx=10, pady=10)
            ctk.CTkLabel(self.runners_frame, text=time, font=NORMAL).grid(row=row_num, column=4, padx=10, pady=10)
            ctk.CTkLabel(self.runners_frame, text="Not implemented", font=NORMAL).grid(row=row_num, column=5, padx=10, pady=10)




