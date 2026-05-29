import customtkinter as ctk
from tkinter import messagebox

HEADER1 = ("Helvetica", 20, "bold")
HEADER2 = ("Helvetica", 18, "bold")
HEADER3 = ("Helvetica", 16, "bold")
NORMAL = ("Helvetica", 14)

RACE_DISTANCES = ["5k", "10k", "10mi", "half marathon", "marathon"]
ALL_RUNNERS = []


class ManualEntryTab:

    def __init__(self, parent):
        parent.grid()
        
    # Tab title
        ctk.CTkLabel(parent, text="Manual Race Entry", font=HEADER1).pack(padx=10, pady=10)

    # Race details frame
        ctk.CTkLabel(parent, text="Race Details", font=HEADER2).pack(padx=10, pady=10)
        race_details = ctk.CTkFrame(parent, border_width=2)
        race_details.pack(padx=10, pady=10)

        # Race name entry
        race_name_frame = ctk.CTkFrame(race_details)
        ctk.CTkLabel(race_name_frame, text="Race Name: ", font=NORMAL).grid(row=0, column=0, padx=10, pady=10)
        self.race_name_entry = ctk.CTkEntry(race_name_frame, font=NORMAL)
        self.race_name_entry.grid(row=0, column=1, padx=10, pady=10)
        race_name_frame.grid(row=0, column=0, padx=10, pady=10)

        # Race distance entry
        race_distance_frame = ctk.CTkFrame(race_details)
        ctk.CTkLabel(race_distance_frame, text="Race Distance: ", font=NORMAL).grid(row=0, column=0, padx=10, pady=10)
        self.race_distance_entry = ctk.CTkComboBox(race_distance_frame, values=RACE_DISTANCES, font=NORMAL)
        self.race_distance_entry.grid(row=0, column=1, padx=10, pady=10)
        race_distance_frame.grid(row=0, column=1, padx=10, pady=10)

        # Race date entry
        race_date_frame = ctk.CTkFrame(race_details)
        ctk.CTkLabel(race_date_frame, text="Race Date: ", font=NORMAL).grid(row=0, column=0, padx=10, pady=10)
        self.race_date_entry = ctk.CTkEntry(race_date_frame, placeholder_text="dd/mm/yy", font=NORMAL)
        self.race_date_entry.grid(row=0, column=1, padx=10, pady=10)
        race_date_frame.grid(row=0, column=2, padx=10, pady=10)

    # Runner details frame
        ctk.CTkLabel(parent, text="Runner Details", font=HEADER2).pack(padx=10, pady=10)
        runner_details = ctk.CTkFrame(parent, border_width=2)
        runner_details.pack(padx=10, pady=10)

        # Runner name entry
        runner_name_frame = ctk.CTkFrame(runner_details)
        ctk.CTkLabel(runner_name_frame, text="Runner Name: ", font=NORMAL).grid(row=0, column=0, padx=10, pady=10)
        self.runner_name_entry = ctk.CTkComboBox(runner_name_frame, values=["Jim Bob"]*10, font=NORMAL)
        self.runner_name_entry.grid(row=0, column=1, padx=10, pady=10)
        runner_name_frame.grid(row=0, column=0, padx=10, pady=10)

        # Runner time entry
        runner_time_frame = ctk.CTkFrame(runner_details)
        ctk.CTkLabel(runner_time_frame, text="Runner Time: ", font=NORMAL).grid(row=0, column=0, padx=10, pady=10)
        self.runner_time_entry = ctk.CTkEntry(runner_time_frame, placeholder_text="hh.mm.ss", font=NORMAL)
        self.runner_time_entry.grid(row=0, column=1, padx=10, pady=10)
        runner_time_frame.grid(row=0, column=1, padx=10, pady=10)

    # Submit button
        ctk.CTkButton(parent, text="Enter result", command=self.submit_clicked, font=HEADER2).pack(padx=10, pady=10)


    def submit_clicked(self):
        race_name = self.race_name_entry.get()
        race_distance = self.race_distance_entry.get()
        race_date = self.race_date_entry.get()

        runner_name = self.runner_name_entry.get()
        runner_time = self.runner_time_entry.get()

        # Input validation

        if race_name == "":
            messagebox.showerror(message="Race name is not valid")
            return

        if race_distance not in RACE_DISTANCES and not race_distance.isnumeric():
            messagebox.showerror(message="Race distance is not valid")
            return
        
        if len(race_date) != 8 or race_date[2] != "/" or race_date[5] != "/" or race_date[8] != "/":
            messagebox.showerror(message="Race date is not valid")
            return
        
        if runner_name not in ALL_RUNNERS:
            messagebox.showerror(message="Runner does not exist")
            return
        
        if len(runner_time) != 8 or runner_time[2] != "." or runner_time[5] != "." or runner_time[8] != ".":
            messagebox.showerror(message="Runner time is invalid")
            return
        
        print(race_name, race_distance, race_date, runner_name, runner_time)

        


    
        