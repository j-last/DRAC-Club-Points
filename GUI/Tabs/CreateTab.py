import customtkinter as ctk
from tkinter import messagebox
from datetime import date

from Database.RunnersTable import RunnersTable
from config import *
from GUI.gui_helper_functions import create_label_entry_pair, clear_entry_box

from Database.RacesTable import RacesTable

class CreateTab:

    def __init__(self, parent, db_conn):
        """Sets up all elements within the 'Create' tab
        """
        self.db_conn = db_conn
        for col in range(6): parent.columnconfigure(col, weight=1)

        # Create a race
        race_frame = ctk.CTkFrame(parent, border_width=2)

        ctk.CTkLabel(race_frame, text="Create Race", font=HEADER1).pack(padx=10, pady=10)

        race_name_frame = ctk.CTkFrame(race_frame)
        self.race_name_entry = create_label_entry_pair(race_name_frame, "Race Name:")
        race_name_frame.pack(padx=10, pady=10)

        race_dist_frame = ctk.CTkFrame(race_frame)
        self.race_dist_entry = create_label_entry_pair(race_dist_frame, "Race Distance:", values=RACE_DISTANCES, state="readonly")
        race_dist_frame.pack(padx=10, pady=10)

        fixed_points_frame = ctk.CTkFrame(race_frame)
        self.fixed_points_entry = create_label_entry_pair(fixed_points_frame, "Fixed Points:", placeholder_text="if applicable")
        fixed_points_frame.pack(padx=10, pady=10)

        race_date_frame = ctk.CTkFrame(race_frame)
        self.race_date_entry = create_label_entry_pair(race_date_frame, "Race Date:", placeholder_text="dd/mm")
        race_date_frame.pack(padx=10, pady=10)

        ctk.CTkButton(race_frame, text="Create Race", command=self.create_race, font=HEADER2).pack(padx=10, pady=10)

        race_frame.grid(row=0, column=2, padx=10, pady=10)

        # Create a runner
        runner_frame = ctk.CTkFrame(parent, border_width=2)

        ctk.CTkLabel(runner_frame, text="Create Runner", font=HEADER1).pack(padx=10, pady=10)

        first_name_frame = ctk.CTkFrame(runner_frame)
        self.first_name_entry = create_label_entry_pair(first_name_frame, "First Name:")
        first_name_frame.pack(padx=10, pady=10)

        last_name_frame = ctk.CTkFrame(runner_frame)
        self.last_name_entry = create_label_entry_pair(last_name_frame, "Last Name:")
        last_name_frame.pack(padx=10, pady=10)

        gender_frame = ctk.CTkFrame(runner_frame)
        self.gender_entry = create_label_entry_pair(gender_frame, "Gender:", values=GENDERS, state="readonly")
        gender_frame.pack(padx=10, pady=10)

        age_cat_frame = ctk.CTkFrame(runner_frame)
        self.age_cat_entry = create_label_entry_pair(age_cat_frame, "Age Category:", values=AGE_CATEGORIES, state="readonly")
        age_cat_frame.pack(padx=10, pady=10)

        ctk.CTkButton(runner_frame, text="Create Runner", command=self.create_runner, font=HEADER2).pack(padx=10, pady=10)
        runner_frame.grid(row=0, column=3, padx=10, pady=10)


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