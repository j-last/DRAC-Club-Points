
import customtkinter as ctk
import pandas as pd
from tkinter import messagebox

from GUI.gui_config import HEADER1, HEADER2, NORMAL

from Database.RunnersTable import RunnersTable

class RacesTab:

    def __init__(self, parent, db_conn):
        """Sets up all elements within the 'View Races' tab
        """
        self.db_conn = db_conn

        ctk.CTkLabel(parent, text="All races", font=HEADER1).pack(padx=10, pady=10)

        races_frame = ctk.CTkScrollableFrame(parent, border_width=2)
        races_frame.pack(padx=10, pady=10, expand=True, fill="both")

        all_races = pd.read_sql("SELECT name, distance, date, fixed_points FROM races ORDER BY date", db_conn).to_numpy()
        for col in range(4): races_frame.grid_columnconfigure(col, weight=1)

        ctk.CTkLabel(races_frame, text="Name", font=HEADER2).grid(row=0, column=0, padx=10)
        ctk.CTkLabel(races_frame, text="Distance",font=HEADER2).grid(row=0, column=1, padx=10)
        ctk.CTkLabel(races_frame, text="Date", font=HEADER2).grid(row=0, column=2, padx=10)
        ctk.CTkLabel(races_frame, text="Points (if fixed)", font=HEADER2).grid(row=0, column=3, padx=10)

        row_val = 1
        for race_name, race_distance, race_date, race_points in all_races:
            if race_distance == None: race_distance = "N/A"
            if race_points == None: race_points = "N/A"
            ctk.CTkLabel(races_frame, text=race_name, font=NORMAL).grid(row=row_val, column=0, padx=10, pady=10)
            ctk.CTkLabel(races_frame, text=race_distance, font=NORMAL).grid(row=row_val, column=1, padx=10, pady=10)
            ctk.CTkLabel(races_frame, text=race_date, font=NORMAL).grid(row=row_val, column=2, padx=10, pady=10)
            ctk.CTkLabel(races_frame, text=race_points, font=NORMAL).grid(row=row_val, column=3, padx=10, pady=10)
            row_val += 1
