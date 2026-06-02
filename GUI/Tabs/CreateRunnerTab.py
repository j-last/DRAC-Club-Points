import customtkinter as ctk

from GUI.gui_config import HEADER1, HEADER2, GENDERS, AGE_CATEGORIES
from GUI.gui_helper_functions import create_label_entry_pair

class CreateRunnerTab:

    def __init__(self, parent, db_conn):
        """Sets up all elements within the 'Create Runner' tab
        """
        self.db_conn = db_conn

        ctk.CTkLabel(parent, text="Create Runner", font=HEADER1).pack(padx=10, pady=10)

        runner_details_frame = ctk.CTkFrame(parent, border_width=2)
        runner_details_frame.pack(padx=10, pady=10)

        first_name_frame = ctk.CTkFrame(runner_details_frame)
        self.first_name_entry = create_label_entry_pair(first_name_frame, "First Name:")
        first_name_frame.pack(padx=10, pady=10)

        last_name_frame = ctk.CTkFrame(runner_details_frame)
        self.last_name_entry = create_label_entry_pair(last_name_frame, "Last Name:")
        last_name_frame.pack(padx=10, pady=10)

        gender_frame = ctk.CTkFrame(runner_details_frame)
        self.gender_entry = create_label_entry_pair(gender_frame, "Gender:", values=GENDERS)
        gender_frame.pack(padx=10, pady=10)

        age_cat_frame = ctk.CTkFrame(runner_details_frame)
        self.age_cat_entry = create_label_entry_pair(age_cat_frame, "Age Category:", values=AGE_CATEGORIES)
        age_cat_frame.pack(padx=10, pady=10)

        ctk.CTkButton(parent, text="Enter result", command=self.submit_clicked, font=HEADER2).pack(padx=10, pady=10)


    def submit_clicked(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        gender = self.gender_entry.get()
        age_cat = self.age_cat_entry.get()

        # Input validation not yet implemented

        
