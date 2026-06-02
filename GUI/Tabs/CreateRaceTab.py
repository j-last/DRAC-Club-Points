import customtkinter as ctk

from GUI.gui_config import HEADER1, RACE_DISTANCES, HEADER2
from GUI.gui_helper_functions import create_label_entry_pair

from Database.RacesTable import RacesTable

class CreateRaceTab:

    def __init__(self, parent, db_conn):
        """Sets up all elements within the 'Create Race' tab
        """
        self.db_conn = db_conn

        ctk.CTkLabel(parent, text="Create Race", font=HEADER1).pack(padx=10, pady=10)

        race_details_frame = ctk.CTkFrame(parent, border_width=2)
        race_details_frame.pack(padx=10, pady=10)

        race_name_frame = ctk.CTkFrame(race_details_frame)
        self.race_name_entry = create_label_entry_pair(race_name_frame, "Race Name:")
        race_name_frame.pack(padx=10, pady=10)

        race_dist_frame = ctk.CTkFrame(race_details_frame)
        self.race_dist_entry = create_label_entry_pair(race_dist_frame, "Race Distance:", values=RACE_DISTANCES)
        race_dist_frame.pack(padx=10, pady=10)

        fixed_points_frame = ctk.CTkFrame(race_details_frame)
        self.fixed_points_entry = create_label_entry_pair(fixed_points_frame, "Fixed Points:", placeholder_text="if applicable")
        fixed_points_frame.pack(padx=10, pady=10)

        race_date_frame = ctk.CTkFrame(race_details_frame)
        self.race_date_entry = create_label_entry_pair(race_date_frame, "Race Date:", placeholder_text="dd/mm/yy")
        race_date_frame.pack(padx=10, pady=10)

        ctk.CTkButton(parent, text="Create Race", command=self.submit_clicked, font=HEADER2).pack(padx=10, pady=10)

    def submit_clicked(self):
        race_name = self.race_name_entry.get()
        race_dist = self.race_dist_entry.get()
        fixed_points = self.fixed_points_entry.get()
        race_date = self.race_date_entry.get()

        # Input validation not yet implemented
        
        if race_dist == "": race_dist = None
        if fixed_points == "": fixed_points = None

        RacesTable.add_entry(self.db_conn, race_name, race_dist, race_date, fixed_points)
