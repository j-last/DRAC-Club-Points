import pandas as pd
import customtkinter as ctk

from config import HEADER3
from Database.RacesTable import RacesTable
from Database.RunnersTable import RunnersTable
from Database.ResultsTable import ResultsTable

class PointsTotalsTab():

    def __init__(self, parent, db_conn):
        """Sets up all elements in the 'Points Totals' tab.
        """
        self.parent = parent
        self.db_conn = db_conn

        self.textbox = ctk.CTkTextbox(parent, border_width=2, font=HEADER3)
        self.textbox.pack(padx=10, pady=10, expand=True, fill="both")

        self.on_focus()

    def on_focus(self):
        """Updates the textbox to include the most up-to-date points totals, in order of highest to lowest points.
        """

        data_rows = []
        
        runners = RunnersTable.get_all(self.db_conn).to_numpy()
        for runner_id, firstname, lastname, _, _ in runners:
            total_points = ResultsTable.get_points_for_runner(self.db_conn, runner_id)
            data_rows.append((total_points, firstname + " " + lastname))
        
        data_rows.sort(reverse=True)
        text = ""
        for points, name in data_rows:
            text += name + " - " + str(points) + "\n"

        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", text)
        self.textbox.configure(state="disabled")
        

            


            
            

