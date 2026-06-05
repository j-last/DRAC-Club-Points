
import customtkinter as ctk
import pandas as pd

from calculate_points import calculate_points
from GUI.gui_config import HEADER1, HEADER2, HEADER3, NORMAL

class RaceViewerTab:

    def __init__(self, parent, db_conn):
        """Sets up all elements within the 'Race Viewer' tab
        """
        self.parent = parent
        self.db_conn = db_conn

        entry_frame = ctk.CTkFrame(parent)
        entry_frame.pack(padx=10, pady=10)
        ctk.CTkLabel(entry_frame, text="Select Race:", font=HEADER2).grid(row=0, column=0, padx=10, pady=10)
        self.race_entry = ctk.CTkComboBox(entry_frame, values=[""], font=NORMAL)
        self.race_entry.grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(entry_frame, text="Find Results", font=HEADER2, command=self.load_results).grid(row=0, column=2, padx=10, pady=10)

        self.num_runners = ctk.CTkLabel(parent, text="")
        self.num_runners.pack(padx=10, pady=10)
        
        self.runners_frame = ctk.CTkScrollableFrame(parent, border_width=2)
        self.runners_frame.pack(padx=10, pady=10, expand=True, fill="both")
        for col in range(5): self.runners_frame.columnconfigure(col, weight=1)

        self.on_focus()


    def on_focus(self):
        """Ensures the 'Select Race:' option box includes the most up-to-date list of races when this tab is selected to.
        """
        self.all_races = {}
        for race_id, name, distance, date in pd.read_sql("""SELECT race_id, name, distance, date FROM races""", self.db_conn).to_numpy():
            if distance is None: distance = ""
            self.all_races[f"{name} {distance} ({date})"] = race_id
        self.race_entry.configure(values=self.all_races.keys())


    def load_results(self):
        """Loads the details of all runners who did the selected race into a table for the user to view.
        """
        race = self.race_entry.get()
        race_id = self.all_races[race]

        runners = pd.read_sql(f"""SELECT runners.runner_id, firstname, lastname, gender, age_category, runner_time
                              FROM runners
                              JOIN race_results ON runners.runner_id = race_results.runner_id
                              WHERE race_results.race_id = {race_id}""", self.db_conn).to_numpy()

        self.num_runners.configure(text=f"{len(runners)} RUNNERS", font=HEADER3)

        for widget in self.runners_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.runners_frame, text="First name", font=HEADER2).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkLabel(self.runners_frame, text="Last name", font=HEADER2).grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkLabel(self.runners_frame, text="Gender", font=HEADER2).grid(row=0, column=2, padx=10, pady=10)
        ctk.CTkLabel(self.runners_frame, text="Age Category", font=HEADER2).grid(row=0, column=3, padx=10, pady=10)
        ctk.CTkLabel(self.runners_frame, text="Time", font=HEADER2).grid(row=0, column=4, padx=10, pady=10)
        ctk.CTkLabel(self.runners_frame, text="Points", font=HEADER2).grid(row=0, column=5, padx=10, pady=10)
        
        row_num = 1
        for runner_id, firstname, lastname, gender, age_cat, runner_time in runners:
            points = calculate_points(runner_id, race_id, runner_time, self.db_conn)
            ctk.CTkLabel(self.runners_frame, text=firstname, font=NORMAL).grid(row=row_num, column=0, padx=10, pady=10)
            ctk.CTkLabel(self.runners_frame, text=lastname, font=NORMAL).grid(row=row_num, column=1, padx=10, pady=10)
            ctk.CTkLabel(self.runners_frame, text=gender, font=NORMAL).grid(row=row_num, column=2, padx=10, pady=10)
            ctk.CTkLabel(self.runners_frame, text=age_cat, font=NORMAL).grid(row=row_num, column=3, padx=10, pady=10)
            ctk.CTkLabel(self.runners_frame, text=runner_time, font=NORMAL).grid(row=row_num, column=4, padx=10, pady=10)
            ctk.CTkLabel(self.runners_frame, text=str(points), font=NORMAL).grid(row=row_num, column=5, padx=10, pady=10)
            row_num += 1




