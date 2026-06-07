import customtkinter as ctk
from tkinter import messagebox

from config import *
from GUI.gui_helper_functions import create_label_entry_pair, clear_entry_box

from Database.RunnersTable import RunnersTable

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
        self.gender_entry = create_label_entry_pair(gender_frame, "Gender:", values=GENDERS, state="readonly")
        gender_frame.pack(padx=10, pady=10)

        age_cat_frame = ctk.CTkFrame(runner_details_frame)
        self.age_cat_entry = create_label_entry_pair(age_cat_frame, "Age Category:", values=AGE_CATEGORIES, state="readonly")
        age_cat_frame.pack(padx=10, pady=10)

        ctk.CTkButton(parent, text="Enter result", command=self.submit_clicked, font=HEADER2).pack(padx=10, pady=10)


    def submit_clicked(self):
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
        