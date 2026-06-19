import customtkinter as ctk

from Database.RacesTable import RacesTable
from Database.RunnersTable import RunnersTable
from GUI.SearchableComboBox import SearchableComboBox
from config import DATE_FORMAT

HEADER1 = ("Helvetica", 20, "bold")
HEADER2 = ("Helvetica", 18, "bold")
HEADER3 = ("Helvetica", 16, "bold")
NORMAL = ("Helvetica", 14)

def create_label_entry_pair(parent:ctk.CTkFrame, text:str, values:list=[], placeholder_text:str="", state:str=ctk.NORMAL):
    """Creates a (CTkLabel, CTkEntry) pair next to each other within the parent frame.
    
    If 'values' is provided, the CTkEntry becomes a CTkComboBox.
    """
    ctk.CTkLabel(parent, text=text, font=NORMAL).grid(row=0, column=0, padx=10, pady=10)
    if len(values) > 0:
        entry_box = SearchableComboBox(parent, values=[""]+values, font=NORMAL, state=state)
    else:
        entry_box = ctk.CTkEntry(parent, font=NORMAL, placeholder_text=placeholder_text)
    entry_box.grid(row=0, column=1, padx=10, pady=10)
    return entry_box

def clear_entry_box(entry_box):
    if type(entry_box) == ctk.CTkEntry:
        entry_box.delete(0, "end")
    elif type(entry_box) == SearchableComboBox:
        entry_box.set("")

def get_race_dict(db_conn):
    """Returns an up-to-date dictionary of all the races in the database in date order.
    
    The keys are the user-selectable options, and the values are the race_id that corresponds with that option.
    """
    race_dict = {}
    for race_id, race_name, race_distance, race_date, _ in RacesTable.get_all(db_conn).to_numpy():
        if race_distance is None: race_distance = ""
        race_date = race_date.strftime(DATE_FORMAT)
        race_dict[f"{race_name} {race_distance} ({race_date})"] = race_id
    return race_dict

def get_runner_dict(db_conn):
    """Returns an up-to-date dictionary of all the runners in the database in alphabetical order.
    
    The keys are the user-selectable options, and the values are the runner_id that corresponds with that option.
    """
    runner_dict = {}
    for runner_id, firstname, lastname, _, _ in RunnersTable.get_all(db_conn).to_numpy():
        runner_dict[f"{firstname} {lastname}"] = runner_id
    return runner_dict

class Table:
    def __init__(self, parent:ctk.CTkScrollableFrame, columns:list[str]):
        """Creates a table within a scrollable frame with the column headings provided.
        """
        self.parent = parent
        self.columns = columns
        self.row_num = 0
        self.parent.pack(padx=10, pady=10, expand=True, fill="both")
        for col in range(len(columns)): self.parent.columnconfigure(col, weight=1)
    

    def clear(self):
        """Clears the table, except for the column headings.
        """
        for widget in self.parent.winfo_children():
            widget.destroy()

        for col_num, col_name in enumerate(self.columns):
            ctk.CTkLabel(self.parent, text=col_name, font=HEADER2).grid(row=0, column=col_num, padx=10, pady=10)
        self.row_num = 1

    def add_row(self, data):
        """Adds a row of data to the bottom of the table
        """
        for col_num, data_val in enumerate(data):
            ctk.CTkLabel(self.parent, text=data_val, font=NORMAL).grid(row=self.row_num, column=col_num, padx=10, pady=10)
        self.row_num += 1
 
