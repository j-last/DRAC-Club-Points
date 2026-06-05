import pandas as pd
import customtkinter as ctk

from GUI.gui_config import HEADER3

class ParkrunsTotalsTab():

    def __init__(self, parent, db_conn):
        self.parent = parent
        self.db_conn = db_conn

        self.textbox = ctk.CTkTextbox(parent, border_width=2, font=HEADER3)
        self.textbox.pack(padx=10, pady=10, expand=True, fill="both")

        self.on_focus()

    def on_focus(self):
        """Updates the textbox to include the most up-to-date points totals, in order of highest to lowest points.
        """

        data_rows = []

        runner_ids = pd.read_sql("SELECT runner_id, firstname, lastname FROM runners", self.db_conn).to_numpy()
        for runner_id, firstname, lastname in runner_ids:
            parkruns = pd.read_sql(f"""SELECT res.race_id
                                    FROM race_results res
                                    JOIN races rs ON res.race_id = rs.race_id
                                    WHERE res.runner_id = {runner_id}
                                    AND rs.name = 'parkrun'""", self.db_conn).to_numpy()
            total_parkruns = len(parkruns)
            data_rows.append((total_parkruns, firstname + " " + lastname))
        
        data_rows.sort(reverse=True)
        text = ""
        for points, name in data_rows:
            text += name + " - " + str(points) + "\n"

        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", text)
        self.textbox.configure(state="disabled")
