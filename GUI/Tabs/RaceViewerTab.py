
from datetime import date

import customtkinter as ctk
import pandas as pd

from Database.RacesTable import RacesTable
from Database.RunnersTable import RunnersTable
from GUI.gui_helper_functions import Table, get_race_dict
from config import *

from Database.ResultsTable import ResultsTable

class RaceViewerTab:

    def __init__(self, parent, db_conn):
        """Sets up all elements within the 'Race Viewer' tab
        """
        self.parent = parent
        self.db_conn = db_conn

        entry_frame = ctk.CTkFrame(parent)
        entry_frame.pack(padx=10, pady=10)
        ctk.CTkLabel(entry_frame, text="Select Race:", font=HEADER2).grid(row=0, column=0, padx=10, pady=10)
        self.race_entry = ctk.CTkComboBox(entry_frame, values=[""], font=NORMAL, command=self.load_results)
        self.race_entry.grid(row=0, column=1, padx=10, pady=10)

        self.num_runners = ctk.CTkLabel(parent, text="")
        self.num_runners.pack(padx=10, pady=10)
        
        runners_frame = ctk.CTkScrollableFrame(parent, border_width=2)
        columns = ["First Name", "Last Name", "Gender", "Age Category", "Time", "Points"]
        self.table = Table(runners_frame, columns)

        self.on_focus()


    def on_focus(self):
        """Ensures the race selector box options and table display data is up-to-date.
        """
        self.race_dict = get_race_dict(self.db_conn)
        self.race_entry.set_options(self.race_dict.keys())

        if self.race_entry.get() != "":
            self.load_results(self.race_entry.get())

    def load_results(self, race_choice):
        """Loads the details of all runners who did the selected race into a table for the user to view.
        """
        race_id = self.race_dict[race_choice]

        runners = RunnersTable.get_all_by_race(self.db_conn, race_id)

        self.num_runners.configure(text=f"{len(runners)} RUNNERS", font=HEADER3)

        self.table.clear()
        
        for runner_id, firstname, lastname, gender, age_cat, result_time in runners.to_numpy():
            points = ResultsTable.get_points_for_result(self.db_conn, runner_id, race_id)
            if result_time is not pd.NaT: result_time = result_time.strftime(TIME_FORMAT)
            self.table.add_row([firstname, lastname, gender, age_cat, result_time, points])
