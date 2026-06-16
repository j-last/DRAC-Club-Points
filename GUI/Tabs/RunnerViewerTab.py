
from datetime import date

import customtkinter as ctk
import pandas as pd

from Database.RacesTable import RacesTable
from GUI.gui_helper_functions import Table
from config import *
from Database.RunnersTable import RunnersTable
from Database.ResultsTable import ResultsTable

class RunnerViewerTab:

    def __init__(self, parent, db_conn):
        """Sets up all elements within the 'Race Viewer' tab
        """
        self.parent = parent
        self.db_conn = db_conn

        entry_frame = ctk.CTkFrame(parent)
        entry_frame.pack(padx=10, pady=10)
        ctk.CTkLabel(entry_frame, text="Select Runner:", font=HEADER2).grid(row=0, column=0, padx=10, pady=10)
        self.runner_entry = ctk.CTkComboBox(entry_frame, values=[""], font=NORMAL)
        self.runner_entry.grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(entry_frame, text="Find Results", font=HEADER2, command=self.load_results).grid(row=0, column=2, padx=10, pady=10)

        self.runner_details = ctk.CTkLabel(parent, text="")
        self.runner_details.pack(padx=10, pady=10)
        
        races_frame = ctk.CTkScrollableFrame(parent, border_width=2)
        columns = ["Name", "Distance", "Date", "Time", "Points"]
        self.table = Table(races_frame, columns)

        self.on_focus()


    def on_focus(self):
        """Ensures the 'Select Runner:' option box includes the most up-to-date list of runners when this tab is selected to.
        """
        self.runner_dict = {}
        for runner_id, firstname, lastname, _, _ in RunnersTable.get_all(self.db_conn).to_numpy():
            self.runner_dict[f"{firstname} {lastname}"] = runner_id
        self.runner_entry.configure(values=self.runner_dict.keys())


    def load_results(self):
        """Loads the details of all races the selected runner has completed into a table for the user to view.
        """
        runner = self.runner_entry.get()
        runner_id = self.runner_dict[runner]

        races = RacesTable.get_all_by_runner(self.db_conn, runner_id)
        total_points = ResultsTable.get_points_for_runner(self.db_conn, runner_id)
        
        self.runner_details.configure(text=f"{len(races)} RACES, {total_points} POINTS", font=HEADER3)

        self.table.clear()
        
        for race_id, name, distance, race_date, _, result_time in races.to_numpy():
            race_date = race_date.strftime(DATE_FORMAT)
            if result_time is not pd.NaT: result_time = result_time.strftime(TIME_FORMAT)
            points = ResultsTable.get_points_for_result(self.db_conn, runner_id, race_id)
            self.table.add_row([name, distance, race_date, result_time, points])
