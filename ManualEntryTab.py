import customtkinter as ctk

HEADER1 = ("Helvetica", 20, "bold")
HEADER2 = ("Helvetica", 18, "bold")
HEADER3 = ("Helvetica", 16, "bold")
NORMAL = ("Helvetica", 14)


class ManualEntryTab:

    def __init__(self, parent):
        
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
        self.race_distance_entry = ctk.CTkComboBox(race_distance_frame, values=["5k", "10k"], font=NORMAL)
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

        parent.grid()

    def submit_clicked(self):
        race_name = self.race_name_entry.get()
        race_distance = self.race_distance_entry.get()
        race_date = self.race_date_entry.get()

        runner_name = self.runner_name_entry.get()
        runner_time = self.runner_time_entry.get()

    
        