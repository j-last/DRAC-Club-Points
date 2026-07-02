import pandas as pd
import customtkinter as ctk

from config import *
from Database.RacesTable import RacesTable
from Database.RunnersTable import RunnersTable
from Database.ResultsTable import ResultsTable

class TotalsTab():

    def __init__(self, parent, db_conn):
        """Sets up all elements in the 'Totals' tab.
        """
        self.db_conn = db_conn

        tab_frame = ctk.CTkFrame(parent)
        tab_frame.pack(padx=10, pady=10, expand=True, fill="both")
        for col in range(2): tab_frame.columnconfigure(col, weight=1)
        tab_frame.rowconfigure(1, weight=1)

        ctk.CTkLabel(tab_frame, text="Points Totals", font=HEADER2).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkLabel(tab_frame, text="Parkrun Totals", font=HEADER2).grid(row=0, column=1, padx=10, pady=10)

        self.points_textbox = ctk.CTkTextbox(tab_frame, border_width=2, font=HEADER3)
        self.points_textbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.parkruns_textbox = ctk.CTkTextbox(tab_frame, border_width=2, font=HEADER3)
        self.parkruns_textbox.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.on_focus()

    def on_focus(self):
        """Updates the textbox to include the most up-to-date totals, in order of highest to lowest.
        """

        points_rows = []
        parkruns_rows = []
        
        runners = RunnersTable.get_all(self.db_conn).to_numpy()
        for runner_id, firstname, lastname, _, _ in runners:
            total_points = ResultsTable.get_points_for_runner(self.db_conn, runner_id)
            points_rows.append((total_points, firstname + " " + lastname))

            all_races = RacesTable.get_all_by_runner(self.db_conn, runner_id)
            total_parkruns = len(all_races[all_races["race_name"] == "parkrun"])
            parkruns_rows.append((total_parkruns, firstname + " " + lastname))
        
        points_rows.sort(reverse=True)
        points_text = ""
        for points, name in points_rows:
            points_text += name + " - " + str(points) + "\n"

        parkruns_rows.sort(reverse=True)
        parkruns_text = ""
        for points, name in parkruns_rows:
            parkruns_text += name + " - " + str(points) + "\n"

        self.points_textbox.configure(state="normal")
        self.points_textbox.delete("0.0", "end")
        self.points_textbox.insert("0.0", points_text)
        self.points_textbox.configure(state="disabled")

        self.parkruns_textbox.configure(state="normal")
        self.parkruns_textbox.delete("0.0", "end")
        self.parkruns_textbox.insert("0.0", parkruns_text)
        self.parkruns_textbox.configure(state="disabled")
