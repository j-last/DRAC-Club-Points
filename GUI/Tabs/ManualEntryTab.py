import customtkinter as ctk
import pandas as pd
from datetime import time, date
from tkinter import messagebox

from config import *
from GUI.gui_helper_functions import create_label_entry_pair, clear_entry_box

from Database.RacesTable import RacesTable
from Database.RunnersTable import RunnersTable
from Database.ResultsTable import ResultsTable

class ManualEntryTab:

    def __init__(self, parent, db_conn):
        """Sets up all elements within the 'Manual Entry' tab.
        """
        self.db_conn = db_conn
        
        ctk.CTkLabel(parent, text="Manual Race Entry", font=HEADER1).pack(padx=10, pady=10)

        manual_entry_frame = ctk.CTkFrame(parent, border_width=2)
        manual_entry_frame.pack(padx=10, pady=10)

        race_frame = ctk.CTkFrame(manual_entry_frame)
        self.race_entry = create_label_entry_pair(race_frame, "Race:", values=[""], state="readonly")
        race_frame.pack(padx=10, pady=10)

        runner_frame = ctk.CTkFrame(manual_entry_frame)
        self.runner_entry = create_label_entry_pair(runner_frame, "Runner:", values=[""], state="readonly")
        runner_frame.pack(padx=10, pady=10)

        runner_time_frame = ctk.CTkFrame(manual_entry_frame)
        self.runner_time_entry = create_label_entry_pair(runner_time_frame, "Runner Time:", placeholder_text="(h.)mm.ss")
        runner_time_frame.pack(padx=10, pady=10)

        ctk.CTkButton(parent, text="Enter result", command=self.submit_clicked, font=HEADER2).pack(padx=10, pady=10)

        self.on_focus()


    def on_focus(self):
        """Ensures the 'Race:' and 'Runner:' option boxes include the most up-to-date list of races and runners 
        when this tab is selected.
        """
        self.race_dict = {}
        for race_id, race_name, race_distance, race_date, _ in RacesTable.get_all(self.db_conn).to_numpy():
            if race_distance is None: race_distance = ""
            race_date = date.strftime(date.strptime(race_date, DATE_FORMAT_DATABASE), DATE_FORMAT)
            self.race_dict[f"{race_name} {race_distance} ({race_date})"] = race_id
        self.race_entry.configure(values=self.race_dict.keys())

        self.runner_dict = {}
        for runner_id, firstname, lastname, _, _ in RunnersTable.get_all(self.db_conn).to_numpy():
            self.runner_dict[f"{firstname} {lastname}"] = runner_id
        self.runner_entry.configure(values=self.runner_dict.keys())


    def submit_clicked(self):
        """Validates GUI input fields and adds the runner, race pair to the database (and a runner time if provided).
        """
        race = self.race_entry.get()
        runner = self.runner_entry.get()
        runner_time = self.runner_time_entry.get().strip()

        race_id = self.race_dict.get(race)
        runner_id = self.runner_dict.get(runner)
        if runner_time == "": runner_time = None
        
        # Input validation/sanitation
        if race_id is None or runner_id is None:
            messagebox.showerror("Race result not made", "Please select options")
            return

        _, _, _, fixed_points = RacesTable.get(self.db_conn, race_id)
        if fixed_points is None and runner_time is None:
            messagebox.showerror("Race result not made", "A race time must be provided for this race")
            return
        
        if runner_time is not None:
            try:
                runner_time = runner_time.split(".")
                if len(runner_time) == 3:
                    runner_time = time(int(runner_time[0]), int(runner_time[1]), int(runner_time[2]))
                elif len(runner_time) == 2:
                    runner_time = time(0, int(runner_time[0]), int(runner_time[1]))
                else: raise ValueError
            except ValueError:
                messagebox.showerror("Race result not made", "Race time is not in an accepted format")
                return

        ResultsTable.add_entry(self.db_conn, runner_id, race_id, runner_time)
        messagebox.showinfo("Result Entered", "Result created successfully")

        clear_entry_box(self.runner_entry)
        clear_entry_box(self.runner_time_entry)
        