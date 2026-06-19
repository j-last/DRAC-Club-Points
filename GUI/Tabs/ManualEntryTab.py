import customtkinter as ctk
import pandas as pd
from datetime import time, date
from tkinter import messagebox

from config import *
from GUI.gui_helper_functions import create_label_entry_pair, clear_entry_box, get_race_dict, get_runner_dict

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
        self.race_entry = create_label_entry_pair(race_frame, "Race:", values=[""])
        race_frame.pack(padx=10, pady=10)
        self.race_entry.bind("<KeyRelease>", self.update_race_options)

        runner_frame = ctk.CTkFrame(manual_entry_frame)
        self.runner_entry = create_label_entry_pair(runner_frame, "Runner:", values=[""])
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
        self.race_dict = get_race_dict(self.db_conn)
        self.race_entry.configure(values=self.race_dict.keys())

        self.runner_dict = get_runner_dict(self.db_conn)
        self.runner_entry.configure(values=self.runner_dict.keys())

    def update_race_options(self, event):
        """Updates the race dropdown options based on what has been typed so far.
        Unfortunately the dropdown cannot be open whilst you type, so after 1 letter the dropdown
        menu opens and you have to reselect the text box.
        """
        text = self.race_entry.get()

        if text == "":
            options = self.race_dict.keys()
        else:
            num_chars = len(text)
            options = [item for item in self.race_dict.keys() if item.lower()[:num_chars] == text.lower()]

        self.race_entry.configure(values=options)
        self.race_entry._open_dropdown_menu()

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
            messagebox.showerror("Race result not made", "Please select valid options")
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
        points_awarded = ResultsTable.get_points_for_result(self.db_conn, runner_id, race_id)
        points_total = ResultsTable.get_points_for_runner(self.db_conn, runner_id)
        messagebox.showinfo("Result Entered", f"{points_awarded} points added to {runner}, Total: {points_total}")

        clear_entry_box(self.runner_entry)
        clear_entry_box(self.runner_time_entry)
        