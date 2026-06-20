import customtkinter as ctk
from tkinter import messagebox
from datetime import date

from Database.RunnersTable import RunnersTable
from GUI.SearchableComboBox import SearchableComboBox
from config import *
from GUI.gui_helper_functions import label_entry_pair, clear_entry_box

from Database.RacesTable import RacesTable

class CreateTab:

    def __init__(self, parent, db_conn):
        """Sets up all elements within the 'Create' tab
        """
        self.db_conn = db_conn
        for col in range(6): parent.columnconfigure(col, weight=1)

        # Create a race (4 entry boxes + a button)
        tab_left_frame = ctk.CTkFrame(parent, border_width=2)

        ctk.CTkLabel(tab_left_frame, text="Create Race", font=HEADER1).pack(padx=10, pady=10)

        self.race_name_entry = label_entry_pair(tab_left_frame, ctk.CTkEntry, text="Race Name:")
        self.race_dist_entry = label_entry_pair(tab_left_frame, ctk.CTkComboBox, text="Race Distance:", values=RACE_DISTANCES, state="readonly")
        self.fixed_points_entry = label_entry_pair(tab_left_frame, ctk.CTkEntry, text="Fixed Points:", placeholder_text="if applicable")
        self.race_date_entry = label_entry_pair(tab_left_frame, ctk.CTkEntry, text="Race Date:", placeholder_text="dd/mm")
        ctk.CTkButton(tab_left_frame, text="Create Race", command=self.create_race, font=HEADER2).pack(padx=10, pady=10)

        tab_left_frame.grid(row=0, column=2, padx=10, pady=10)

        # Create a runner (4 entry boxes + a button)
        tab_right_frame = ctk.CTkFrame(parent, border_width=2)

        ctk.CTkLabel(tab_right_frame, text="Create Runner", font=HEADER1).pack(padx=10, pady=10)

        self.first_name_entry = label_entry_pair(tab_right_frame, ctk.CTkEntry, text="First Name:")
        self.last_name_entry = label_entry_pair(tab_right_frame, ctk.CTkEntry, text="Last Name:")
        self.gender_entry = label_entry_pair(tab_right_frame, ctk.CTkComboBox, text="Gender:", values=GENDERS, state="readonly")
        self.age_cat_entry = label_entry_pair(tab_right_frame, ctk.CTkComboBox, text="Age Category:", values=AGE_CATEGORIES, state="readonly")
        ctk.CTkButton(tab_right_frame, text="Create Runner", command=self.create_runner, font=HEADER2).pack(padx=10, pady=10)

        tab_right_frame.grid(row=0, column=3, padx=10, pady=10)


    def create_race(self):
        """Validates GUI input fields and adds the race details entered to the database.
        """
        race_name = self.race_name_entry.get().strip()
        race_dist = self.race_dist_entry.get().strip()
        race_date = self.race_date_entry.get().strip()
        race_points = self.fixed_points_entry.get().strip()

        # Input validation
        if race_name == "" or race_dist == "" or race_date == "": 
            messagebox.showerror("Race not created", "A box has been left blank")
            return
        try:
            race_date = date(2026, int(race_date[-2:]), int(race_date[0:2]))
        except ValueError:
            messagebox.showerror("Race not created", "Race date is not in the correct format (dd/mm/yyyy)")
            return
        if race_dist == "other" and race_points == "":
            messagebox.showerror("Race not created", "Fixed points must be provided if race distance is 'other'")
            return
        if race_points != "" and not race_points.isnumeric():
            messagebox.showerror("Race not created", "Race points must be left blank or a whole number")
            return
        
        if race_points == "": race_points = None
        else: race_points = int(race_points)
        
        RacesTable.add_entry(self.db_conn, race_name, race_dist, race_date, race_points)
        messagebox.showinfo("Race Created", f"{race_name} {race_dist} created successfully")

        clear_entry_box(self.race_name_entry)
        clear_entry_box(self.fixed_points_entry)
        clear_entry_box(self.race_dist_entry)
        clear_entry_box(self.race_date_entry)


    def create_runner(self):
        """Validates GUI input fields and adds the runner details entered to the database.
        """
        firstname = self.first_name_entry.get().strip().capitalize()
        lastname = self.last_name_entry.get().strip().capitalize()
        gender = self.gender_entry.get().strip()
        age_cat = self.age_cat_entry.get().strip()

        # Input validation/sanitation
        if firstname == "" or lastname == "" or gender == "" or age_cat == "":
            messagebox.showerror("Runner not created", "A box has been left blank")
            return
        if firstname.find(" ") != -1 or lastname.find(" ") != -1:
            messagebox.showerror("Runner not created", "Runner name cannot have spaces")
            return
        
        RunnersTable.add_entry(self.db_conn, firstname, lastname, gender, age_cat)
        messagebox.showinfo("Runner Created", f"{firstname} {lastname} created successfully")

        clear_entry_box(self.first_name_entry)
        clear_entry_box(self.last_name_entry)
        clear_entry_box(self.gender_entry)
        clear_entry_box(self.age_cat_entry)