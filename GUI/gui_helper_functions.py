import customtkinter as ctk

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
        entry_box = ctk.CTkComboBox(parent, values=[""]+values, font=NORMAL, state=state)
    else:
        entry_box = ctk.CTkEntry(parent, font=NORMAL, placeholder_text=placeholder_text)
    entry_box.grid(row=0, column=1, padx=10, pady=10)
    return entry_box

def clear_entry_box(entry_box):
    if type(entry_box) == ctk.CTkEntry:
        entry_box.delete(0, "end")
    elif type(entry_box) == ctk.CTkComboBox:
        entry_box.set("")

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
 
