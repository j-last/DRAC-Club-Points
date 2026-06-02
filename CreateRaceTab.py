import customtkinter as ctk
from helper_functions import create_label_entry_pair

HEADER1 = ("Helvetica", 20, "bold")
HEADER2 = ("Helvetica", 18, "bold")
HEADER3 = ("Helvetica", 16, "bold")
NORMAL = ("Helvetica", 14)
RACE_DISTANCES = ["5k", "10k", "10mi", "half marathon", "marathon"]

class CreateRaceTab:

    def __init__(self, parent):
        """Sets up all elements within the 'Create Race' tab
        """

        ctk.CTkLabel(parent, text="Create Race", font=HEADER1).pack(padx=10, pady=10)

        race_details_frame = ctk.CTkFrame(parent, border_width=2)
        race_details_frame.pack(padx=10, pady=10)

        race_name_frame = ctk.CTkFrame(race_details_frame)
        self.race_name_entry = create_label_entry_pair(race_name_frame, "Race Name:")
        race_name_frame.pack(padx=10, pady=10)

        race_dist_frame = ctk.CTkFrame(race_details_frame)
        self.race_dist_entry = create_label_entry_pair(race_dist_frame, "Race Distance:", values=RACE_DISTANCES)
        race_dist_frame.pack(padx=10, pady=10)

        race_date_frame = ctk.CTkFrame(race_details_frame)
        self.race_date_entry = create_label_entry_pair(race_date_frame, "Race Date:", placeholder_text="dd/mm/yy")
        race_date_frame.pack(padx=10, pady=10)

        ctk.CTkButton(parent, text="Create Race", command=self.submit_clicked, font=HEADER2).pack(padx=10, pady=10)


    def submit_clicked(self):
        race_name = self.race_name_entry.get()
        race_dist = self.race_dist_entry.get()
        race_date = self.race_date_entry.get()
