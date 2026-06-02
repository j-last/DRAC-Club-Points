import customtkinter as ctk

HEADER1 = ("Helvetica", 20, "bold")
HEADER2 = ("Helvetica", 18, "bold")
HEADER3 = ("Helvetica", 16, "bold")
NORMAL = ("Helvetica", 14)

def create_label_entry_pair(parent, text, values=[], placeholder_text=""):
    """Creates a (CTkLabel, CTkEntry) pair nect to each other within the parent frame.
    
    If values is provided, the CTkEntry becomes a CTkComboBox, with the values as the options.
    """
    ctk.CTkLabel(parent, text=text, font=NORMAL).grid(row=0, column=0, padx=10, pady=10)
    if len(values) > 0:
        entry_box = ctk.CTkComboBox(parent, values=values, font=NORMAL)
    else:
        entry_box = ctk.CTkEntry(parent, font=NORMAL, placeholder_text=placeholder_text)
    entry_box.grid(row=0, column=1, padx=10, pady=10)
    return entry_box