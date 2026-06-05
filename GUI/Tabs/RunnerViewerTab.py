
import customtkinter as ctk
import pandas as pd

from helper_functions import calculate_points
from config import HEADER1, HEADER2, HEADER3, NORMAL

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
        
        self.races_frame = ctk.CTkScrollableFrame(parent, border_width=2)
        self.races_frame.pack(padx=10, pady=10, expand=True, fill="both")
        for col in range(5): self.races_frame.columnconfigure(col, weight=1)

        self.on_focus()


    def on_focus(self):
        """Ensures the 'Select Runner:' option box includes the most up-to-date list of runners when this tab is selected to.
        """
        self.all_runners = {}
        for runner_id, firstname, lastname, gender, age_category in pd.read_sql("""SELECT runner_id, firstname, lastname, gender, age_category FROM runners""", self.db_conn).to_numpy():
            self.all_runners[f"{firstname} {lastname} ({gender} {age_category})"] = runner_id
        self.runner_entry.configure(values=self.all_runners.keys())


    def load_results(self):
        """Loads the details of all races the selected runner has completed into a table for the user to view.
        """
        runner = self.runner_entry.get()
        runner_id = self.all_runners[runner]

        races = pd.read_sql(f"""SELECT races.race_id, name, distance, date, runner_time
                              FROM races
                              JOIN race_results ON races.race_id = race_results.race_id
                              WHERE race_results.runner_id = {runner_id}""", self.db_conn).to_numpy()

        for widget in self.races_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.races_frame, text="Name", font=HEADER2).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkLabel(self.races_frame, text="Distance", font=HEADER2).grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkLabel(self.races_frame, text="Date", font=HEADER2).grid(row=0, column=2, padx=10, pady=10)
        ctk.CTkLabel(self.races_frame, text="Time", font=HEADER2).grid(row=0, column=3, padx=10, pady=10)
        ctk.CTkLabel(self.races_frame, text="Points", font=HEADER2).grid(row=0, column=4, padx=10, pady=10)
        
        row_num = 1
        total_points = 0
        for race_id, name, distance, date, runner_time in races:
            points = calculate_points(runner_id, race_id, runner_time, self.db_conn)
            total_points += points
            ctk.CTkLabel(self.races_frame, text=name, font=NORMAL).grid(row=row_num, column=0, padx=10, pady=10)
            ctk.CTkLabel(self.races_frame, text=distance, font=NORMAL).grid(row=row_num, column=1, padx=10, pady=10)
            ctk.CTkLabel(self.races_frame, text=date, font=NORMAL).grid(row=row_num, column=2, padx=10, pady=10)
            ctk.CTkLabel(self.races_frame, text=runner_time, font=NORMAL).grid(row=row_num, column=3, padx=10, pady=10)
            ctk.CTkLabel(self.races_frame, text=str(points), font=NORMAL).grid(row=row_num, column=4, padx=10, pady=10)
        
        self.runner_details.configure(text=f"{len(races)} RACES, {total_points} POINTS", font=HEADER3)
