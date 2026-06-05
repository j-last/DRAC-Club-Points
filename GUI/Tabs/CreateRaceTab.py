import customtkinter as ctk
from tkinter import messagebox
from datetime import date

from GUI.gui_config import HEADER1, RACE_DISTANCES, HEADER2
from GUI.gui_helper_functions import create_label_entry_pair, clear_entry_box

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
        self.race_dist_entry = create_label_entry_pair(race_dist_frame, "Race Distance:", values=RACE_DISTANCES, state="readonly")
        race_dist_frame.pack(padx=10, pady=10)

        fixed_points_frame = ctk.CTkFrame(race_details_frame)
        self.fixed_points_entry = create_label_entry_pair(fixed_points_frame, "Fixed Points:", placeholder_text="if applicable")
        fixed_points_frame.pack(padx=10, pady=10)

        race_date_frame = ctk.CTkFrame(race_details_frame)
        self.race_date_entry = create_label_entry_pair(race_date_frame, "Race Date:", placeholder_text="dd/mm/yy")
        race_date_frame.pack(padx=10, pady=10)

        ctk.CTkButton(parent, text="Create Race", command=self.submit_clicked, font=HEADER2).pack(padx=10, pady=10)


    def submit_clicked(self):
        """Validates GUI input fields and adds the race details entered to the database.
        """
        race_name = self.race_name_entry.get()
        race_dist = self.race_dist_entry.get()
        race_points = self.fixed_points_entry.get()
        race_date = self.race_date_entry.get()

        # Input validation / sanitation
        if race_name == "": 
            messagebox.showerror("Race not created", "Race name cannot be blank")
            return
        if race_dist not in RACE_DISTANCES: 
            messagebox.showerror("Race not created", "Race distance is not valid")
            return
        if race_dist == "other" and race_points == "":
            messagebox.showerror("Race not created", "Fixed points must be provided if race distance is 'other'")
            return
        if race_points != "" and not race_points.isnumeric():
            messagebox.showerror("Race not created", "Race points must be either left blank or a whole number")
            return
        try:
            race_date = date(int(race_date[-4:]), int(race_date[3:5]), int(race_date[0:2]))
        except ValueError:
            messagebox.showerror("Race not created", "Race date is not in the correct format (dd/mm/yyyy)")
            return
        
        if race_points == "": race_points = None
        else: race_points = int(race_points)
        
        RacesTable.add_entry(self.db_conn, race_name, race_dist, race_date, race_points)
        messagebox.showinfo("Race Created", "Race created successfully")

        clear_entry_box(self.race_name_entry)
        clear_entry_box(self.fixed_points_entry)
        clear_entry_box(self.race_dist_entry)
        clear_entry_box(self.race_date_entry)
