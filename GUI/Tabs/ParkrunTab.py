from tkinter import messagebox

import customtkinter as ctk
import pandas as pd
from datetime import date, time

from Database.RacesTable import RacesTable
from Database.ResultsTable import ResultsTable
from Database.RunnersTable import RunnersTable
from GUI.SearchableComboBox import SearchableComboBox
from config import *
from GUI.gui_helper_functions import label_entry_pair, clear_entry_box, get_race_dict, get_runner_dict
from helper_functions import get_total_race_timings_results


class ParkrunTab:

    def __init__(self, parent, db_conn):
        """Sets up all elements in the 'Total Race Timing' tab.
        """
        self.db_conn = db_conn
        
        ctk.CTkLabel(parent, text="Automatic Parkrun Entry", font=HEADER1).pack(padx=10, pady=10)
    
    # CHANGE BACK - NEED TO MAKE A RACE IN ORDER TO GET POINTS?
        self.date_entry = label_entry_pair(parent, ctk.CTkEntry, text="Date:", placeholder_text="dd/mm")

        self.parkrun_text_entry = label_entry_pair(parent, ctk.CTkEntry, text="Parkrun text:")
        ctk.CTkButton(self.parkrun_text_entry.master, text="Get Results", font=HEADER3, command=self.get_results).grid(row=0, column=2, padx=10, pady=10)

        self.results_frame = ctk.CTkScrollableFrame(parent, border_width=2)
        for col in range(2): self.results_frame.columnconfigure(col, weight=1)
        self.results_frame.pack(padx=10, pady=10, expand=True, fill="both")
        self.runner_entry_boxes = []

        self.on_focus()


    def on_focus(self):
        """Ensures the 'Race:' and 'Runner:' option boxes include the most up-to-date list of races and runners 
        when this tab is selected.
        """
        self.runner_dict = get_runner_dict(self.db_conn)
        for runner_entry in self.runner_entry_boxes:
            runner_entry.configure(values=self.runner_dict.keys())


    def get_results(self):
        parkrun_text = self.parkrun_text_entry.get()

        runners = [] # To do (function to return all names of people who did parkrun)

        for widget in self.results_frame.winfo_children():
            widget.destroy()
        self.runner_entry_boxes = []
        self.time_entry_boxes = []

        ctk.CTkLabel(self.results_frame, text="Name", font=HEADER2).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkLabel(self.results_frame, text="Select runner", font=HEADER2).grid(row=0, column=2, padx=10, pady=10)

        row_num = 1
        for runner_name in runners:
            ctk.CTkLabel(self.results_frame, text=runner_name, font=NORMAL).grid(row=row_num, column=0, padx=10, pady=10)

            runner_entry = ctk.CTkComboBox(self.results_frame, font=NORMAL, state="readonly")
            if runner_name in self.runner_dict.keys():
                runner_entry.set(runner_name)
                runner_entry.configure(fg_color="green")
            else:
                runner_entry.configure(fg_color="red")
            runner_entry.grid(row=row_num, column=2, padx=10, pady=10)
            self.runner_entry_boxes.append(runner_entry)

            row_num += 1
        
        ctk.CTkButton(self.results_frame, text="Add results", font=HEADER2, command=self.add_results).grid(row=row_num, column=2, padx=10, pady=10)

        self.on_focus()

    def add_results(self):
        race = self.race_entry.get()
        race_id = self.race_dict.get(race)
        if race_id is None:
            messagebox.showerror("Results not added", "Please select a race")
            return
        
        runner_names = []
        runner_ids = []
        for runner_entry_box in self.runner_entry_boxes:
            runner = runner_entry_box.get()
            runner_names.append(runner)
            runner_ids.append(self.runner_dict.get(runner))
        if None in runner_ids:
            if not messagebox.askokcancel("Proceed?", f"{runner_ids.count(None)} runner selection boxes are blank. No result will be added for these runners. Proceed?"):
                messagebox.showerror("Results not added", "No results added")
                return
        
        messagebox_str = "Parkruns added to:\n"
        for runner_id, runner_name in zip(runner_ids, runner_names):
            if runner_id is not None:
                ResultsTable.add_entry(self.db_conn, runner_id, race_id, None)
                messagebox_str += f"{runner_name}\n"
        
        messagebox.showinfo("Results Entered", messagebox_str)

        

