import customtkinter as ctk
import pandas as pd
from datetime import time, date
from tkinter import messagebox

from config import HEADER1, HEADER2, HEADER3, NORMAL, DATE_FORMAT
from GUI.gui_helper_functions import create_label_entry_pair, clear_entry_box
from helper_functions import get_total_race_timings_results


class TotalRaceTimingTab:

    def __init__(self, parent, db_conn):
        """Sets up all elements in the 'Total Race Timing' tab.
        """
        self.db_conn = db_conn
        
        ctk.CTkLabel(parent, text="Total Race Timing Link Entry", font=HEADER1).pack(padx=10, pady=10)


        race_entry_frame = ctk.CTkFrame(parent)
        self.race_entry = create_label_entry_pair(race_entry_frame, "Race:", values=[""], state="readonly")
        race_entry_frame.pack(padx=10, pady=10)

        link_entry_frame = ctk.CTkFrame(parent, border_width=2)
        self.link_entry = create_label_entry_pair(link_entry_frame, "Link:")
        ctk.CTkButton(link_entry_frame, text="Get Results", font=HEADER3, command=self.get_results).grid(row=0, column=2, padx=10, pady=10)
        link_entry_frame.pack(padx=10, pady=10)

        self.results_frame = ctk.CTkScrollableFrame(parent, border_width=2)
        for col in range(5): self.results_frame.columnconfigure(col, weight=1)
        self.results_frame.pack(padx=10, pady=10, expand=True, fill="both")

        self.on_focus()


    def on_focus(self):
        """Ensures the 'Race:' and 'Runner:' option boxes include the most up-to-date list of races and runners 
        when this tab is selected.
        """
        self.all_races = {}
        for race_id, name, distance, race_date in pd.read_sql("""SELECT race_id, name, distance, date FROM races""", self.db_conn).to_numpy():
            if distance is None: distance = ""
            race_date = date.strptime(race_date, "%Y-%m-%d")
            race_date = race_date.strftime(DATE_FORMAT)
            self.all_races[f"{name} {distance} ({race_date})"] = race_id
        self.race_entry.configure(values=self.all_races.keys())


    def get_results(self):
        url = self.link_entry.get()

        results = get_total_race_timings_results(url)

        for widget in self.results_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.results_frame, text="Name", font=HEADER2).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkLabel(self.results_frame, text="Time", font=HEADER2).grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkLabel(self.results_frame, text="Select runner", font=HEADER2).grid(row=0, column=2, padx=10, pady=10)
        ctk.CTkLabel(self.results_frame, text="Points", font=HEADER2).grid(row=0, column=3, padx=10, pady=10)

        row_num = 1
        for name, time in zip(results.keys(), results.values()):
            ctk.CTkLabel(self.results_frame, text=name, font=NORMAL).grid(row=row_num, column=0, padx=10, pady=10)
            ctk.CTkLabel(self.results_frame, text=time, font=NORMAL).grid(row=row_num, column=1, padx=10, pady=10)
            row_num += 1
        
        ctk.CTkButton(self.results_frame, text="Add results", font=HEADER2, command=self.add_results).grid(row=row_num, column=2, padx=10, pady=10)


    def add_results(self):
        pass
