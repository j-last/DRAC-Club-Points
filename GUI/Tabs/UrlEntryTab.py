from tkinter import messagebox

import customtkinter as ctk
import pandas as pd
from datetime import date, time

from Database.RacesTable import RacesTable
from Database.ResultsTable import ResultsTable
from Database.RunnersTable import RunnersTable
from config import *
from GUI.gui_helper_functions import create_label_entry_pair, clear_entry_box, get_race_dict, get_runner_dict
from helper_functions import get_total_race_timings_results


class UrlEntryTab:

    def __init__(self, parent, db_conn):
        """Sets up all elements in the 'Total Race Timing' tab.
        """
        self.db_conn = db_conn
        
        ctk.CTkLabel(parent, text="Total Race Timing Link Entry", font=HEADER1).pack(padx=10, pady=10)

        race_entry_frame = ctk.CTkFrame(parent)
        self.race_entry = create_label_entry_pair(race_entry_frame, "Race:", values=[""], state="readonly")
        race_entry_frame.pack(padx=10, pady=10)

        link_entry_frame = ctk.CTkFrame(parent, border_width=2)
        self.link_entry = create_label_entry_pair(link_entry_frame, "Link:")
        ctk.CTkButton(link_entry_frame, text="Get Results", font=HEADER3, command=self.get_results).grid(row=0, column=2, padx=10, pady=10)
        link_entry_frame.pack(padx=10, pady=10)

        self.results_frame = ctk.CTkScrollableFrame(parent, border_width=2)
        for col in range(3): self.results_frame.columnconfigure(col, weight=1)
        self.results_frame.pack(padx=10, pady=10, expand=True, fill="both")
        self.runner_entry_boxes = []
        self.time_entry_boxes = []

        self.on_focus()


    def on_focus(self):
        """Ensures the 'Race:' and 'Runner:' option boxes include the most up-to-date list of races and runners 
        when this tab is selected.
        """
        self.race_dict = get_race_dict(self.db_conn)
        self.race_entry.set_options(self.race_dict.keys())

        self.runner_dict = get_runner_dict(self.db_conn)
        for runner_entry in self.runner_entry_boxes:
            runner_entry.configure(values=self.runner_dict.keys())


    def get_results(self):
        url = self.link_entry.get()

        results = get_total_race_timings_results(url)

        for widget in self.results_frame.winfo_children():
            widget.destroy()
        self.runner_entry_boxes = []
        self.time_entry_boxes = []

        ctk.CTkLabel(self.results_frame, text="Name", font=HEADER2).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkLabel(self.results_frame, text="Time", font=HEADER2).grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkLabel(self.results_frame, text="Select runner", font=HEADER2).grid(row=0, column=2, padx=10, pady=10)

        row_num = 1
        for runner_name, result_time in zip(results.keys(), results.values()):
            ctk.CTkLabel(self.results_frame, text=runner_name, font=NORMAL).grid(row=row_num, column=0, padx=10, pady=10)

            time_entry = ctk.CTkEntry(self.results_frame, font=NORMAL)
            time_entry.insert(0, result_time)
            time_entry.grid(row=row_num, column=1, padx=10, pady=10)
            self.time_entry_boxes.append(time_entry)

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
        
        result_times = []
        for time_entry_box in self.time_entry_boxes:
            result_time_str = time_entry_box.get()
            try:
                result_time = time.strptime(result_time_str, TIME_FORMAT)
                result_times.append(result_time)
            except ValueError:
                messagebox.showerror("Race result not made", f"{result_time_str} is not in the format HH:MM:SS")
                return
        
        messagebox_str = ""
        for runner_id, result_time, runner_name in zip(runner_ids, result_times, runner_names):
            if runner_id is not None:
                ResultsTable.add_entry(self.db_conn, runner_id, race_id, result_time)
                points_awarded = ResultsTable.get_points_for_result(self.db_conn, runner_id, race_id)
                points_total = ResultsTable.get_points_for_runner(self.db_conn, runner_id)
                messagebox_str += f"{points_awarded} points added to {runner_name}, Total: {points_total}\n"
        
        messagebox.showinfo("Results Entered", messagebox_str)

        

