import customtkinter as ctk
import pandas as pd
from datetime import time, date
from tkinter import messagebox

from GUI.gui_config import HEADER1, HEADER2, TIME_FORMAT, DATE_FORMAT
from GUI.gui_helper_functions import create_label_entry_pair, clear_entry_box

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
        self.all_races = {}
        for race_id, name, distance, race_date in pd.read_sql("""SELECT race_id, name, distance, date FROM races""", self.db_conn).to_numpy():
            if distance is None: distance = ""
            race_date = date.strptime(race_date, "%Y-%m-%d")
            race_date = race_date.strftime(DATE_FORMAT)
            self.all_races[f"{name} {distance} ({race_date})"] = race_id
        self.race_entry.configure(values=self.all_races.keys())

        self.all_runners = {}
        for runner_id, firstname, lastname in pd.read_sql("""SELECT runner_id, firstname, lastname FROM runners""", self.db_conn).to_numpy():
            self.all_runners[f"{firstname} {lastname}"] = runner_id
        self.runner_entry.configure(values=self.all_runners.keys())


    def submit_clicked(self):
        """Validates GUI input fields and adds the runner, race pair to the database (and a runner time if provided).
        """
        race = self.race_entry.get().strip()
        runner = self.runner_entry.get().strip()
        runner_time = self.runner_time_entry.get().strip()

        race_id = self.all_races.get(race)
        runner_id = self.all_runners.get(runner)
        
        # Input validation/sanitation
        if race_id is None:
            messagebox.showerror("Race result not made", "Please select a valid race from the options")
            return
        if runner_id is None:
            messagebox.showerror("Race result not made", "Please select a valid runner from the options")
            return

        fixed_points = pd.read_sql(f"SELECT fixed_points FROM races WHERE race_id={race_id}", self.db_conn).to_numpy()[0][0]
        if fixed_points is None and runner_time == "":
            messagebox.showerror("Race result not made", "A race time must be provided for this race")
            return
        
        if runner_time != "":
            try:
                runner_time = runner_time.split(".")
                if len(runner_time) == 3:
                    runner_time = time(int(runner_time[0]), int(runner_time[1]), int(runner_time[2]))
                elif len(runner_time) == 2:
                    runner_time = time(0, int(runner_time[0]), int(runner_time[1]))
                else:
                    messagebox.showerror("Race result not made", "Race time is not in an accepted format")
                    return
            except ValueError:
                messagebox.showerror("Race result not made", "Race time is not in an accepted format")
                return
            
        if runner_time == "": runner_time = None
        else: runner_time = runner_time.strftime(TIME_FORMAT)

        RaceResultsTable.add_entry(self.db_conn, runner_id, race_id, runner_time)
        messagebox.showinfo("Result Entered", "Result created successfully")

        clear_entry_box(self.runner_entry)
        clear_entry_box(self.runner_time_entry)

        