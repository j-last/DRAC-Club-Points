import customtkinter as ctk
from tkinter import messagebox
from datetime import date

from Database.RunnersTable import RunnersTable
from GUI.SearchableComboBox import SearchableComboBox
from config import *
from GUI.gui_helper_functions import get_race_dict, get_runner_dict, label_entry_pair, clear_entry_box

from Database.RacesTable import RacesTable

class EditTab:

    def __init__(self, parent, db_conn):
        """Sets up all elements within the 'Edit Race/Runner' tab
        """
        self.db_conn = db_conn
        for col in range(6): parent.columnconfigure(col, weight=1)

        # Edit race (5 entry boxes + a button)
        tab_left_frame = ctk.CTkFrame(parent, border_width=2)

        ctk.CTkLabel(tab_left_frame, text="Edit/Delete Race", font=HEADER1).pack(padx=10, pady=10)

        self.race_entry = label_entry_pair(tab_left_frame, SearchableComboBox, text="Race to edit:")
        self.race_name_entry = label_entry_pair(tab_left_frame, ctk.CTkEntry, text="Race Name:")
        self.race_dist_entry = label_entry_pair(tab_left_frame, ctk.CTkComboBox, text="Race Distance:", values=RACE_DISTANCES, state="readonly")
        self.fixed_points_entry = label_entry_pair(tab_left_frame, ctk.CTkEntry, text="Fixed Points:", placeholder_text="if applicable")
        self.race_date_entry = label_entry_pair(tab_left_frame, ctk.CTkEntry, text="Race Date:", placeholder_text="dd/mm")
        ctk.CTkButton(tab_left_frame, text="Update Race", command=self.edit_race, font=HEADER2).pack(padx=10, pady=10)

        tab_left_frame.grid(row=0, column=2, padx=10, pady=10)

        # Edit runner (5 entry boxes + a button)
        tab_right_frame = ctk.CTkFrame(parent, border_width=2)

        ctk.CTkLabel(tab_right_frame, text="Edit/Delete Runner", font=HEADER1).pack(padx=10, pady=10)

        self.runner_entry = label_entry_pair(tab_right_frame, SearchableComboBox, text="Runner:")
        self.first_name_entry = label_entry_pair(tab_right_frame, ctk.CTkEntry, text="First Name:")
        self.last_name_entry = label_entry_pair(tab_right_frame, ctk.CTkEntry, text="Last Name:")
        self.gender_entry = label_entry_pair(tab_right_frame, ctk.CTkComboBox, text="Gender:", values=GENDERS, state="readonly")
        self.age_cat_entry = label_entry_pair(tab_right_frame, ctk.CTkComboBox, text="Age Category:", values=AGE_CATEGORIES, state="readonly")
        ctk.CTkButton(tab_right_frame, text="Update Runner", command=self.edit_runner, font=HEADER2).pack(padx=10, pady=10)

        tab_right_frame.grid(row=0, column=3, padx=10, pady=10)

    def on_focus(self):
        """Ensures the 'Race:' and 'Runner:' option boxes include the most up-to-date list of races and runners 
        when this tab is selected.
        """
        self.race_dict = get_race_dict(self.db_conn)
        self.race_entry.set_options(list(self.race_dict.keys()))

        self.runner_dict = get_runner_dict(self.db_conn)
        self.runner_entry.set_options(list(self.runner_dict.keys()))

    def edit_race(self):
        """Validates GUI input fields and updates the specified race in the database
        """
        race = self.race_entry.get()
        race_name = self.race_name_entry.get().strip()
        race_dist = self.race_dist_entry.get()
        race_date = self.race_date_entry.get().strip()
        race_points = self.fixed_points_entry.get().strip()

        race_id = self.race_dict.get(race)
        # Input validation
        if race_id is None:
            messagebox.showerror("Race not updated", "Please select a race to update")
            return
        if race_name == "" or race_dist == "" or race_date == "": 
            messagebox.showerror("Race not created", "A box has been left blank")
            return
        try:
            race_date = date(2026, int(race_date[-2:]), int(race_date[0:2]))
        except ValueError:
            messagebox.showerror("Race not updated", "Race date is not in the correct format (dd/mm/yyyy)")
            return
        if race_dist == "Other" and race_points == "":
            messagebox.showerror("Race not updated", "Fixed points must be provided if race distance is 'Other'")
            return
        if race_points != "" and not race_points.isnumeric():
            messagebox.showerror("Race not updated", "Race points must be left blank or a whole number")
            return
        
        if race_points == "": race_points = None
        else: race_points = int(race_points)
        
        RacesTable.update_entry(self.db_conn, race_id, race_name, race_dist, race_date, race_points)
        messagebox.showinfo("Race Updated", f"{race_name} {race_dist} updated successfully")

        clear_entry_box(self.race_entry)
        clear_entry_box(self.race_name_entry)
        clear_entry_box(self.fixed_points_entry)
        clear_entry_box(self.race_dist_entry)
        clear_entry_box(self.race_date_entry)

    def edit_runner(self):
        """Validates GUI input fields and updates the specified runner in the database
        """
        runner = self.runner_entry.get()
        firstname = self.first_name_entry.get().strip().capitalize()
        lastname = self.last_name_entry.get().strip().capitalize()
        gender = self.gender_entry.get().strip()
        age_cat = self.age_cat_entry.get().strip()

        runner_id = self.runner_dict.get(runner)
        # Input validation/sanitation
        if runner_id is None:
            messagebox.showerror("Runner not updated", "Please select a runner to update")
            return
        if firstname == "" or lastname == "" or gender == "" or age_cat == "":
            messagebox.showerror("Runner not created", "A box has been left blank")
            return
        if firstname.find(" ") != -1 or lastname.find(" ") != -1:
            messagebox.showerror("Runner not created", "Runner name cannot have spaces")
            return
        
        RunnersTable.update_entry(self.db_conn, runner_id, firstname, lastname, gender, age_cat)
        messagebox.showinfo("Runner Updated", f"{firstname} {lastname} updated successfully")

        clear_entry_box(self.runner_entry)
        clear_entry_box(self.first_name_entry)
        clear_entry_box(self.last_name_entry)
        clear_entry_box(self.gender_entry)
        clear_entry_box(self.age_cat_entry)