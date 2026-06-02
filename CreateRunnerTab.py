import customtkinter as ctk

HEADER1 = ("Helvetica", 20, "bold")
HEADER2 = ("Helvetica", 18, "bold")
HEADER3 = ("Helvetica", 16, "bold")
NORMAL = ("Helvetica", 14)

class CreateRunnerTab:

    def __init__(self, parent):

    # Tab title
        ctk.CTkLabel(parent, text="Create Runner", font=HEADER1).pack(padx=10, pady=10)

        # Runner firstname entry
        firstname_frame = ctk.CTkFrame(parent)
        ctk.CTkLabel(firstname_frame, text="First Name: ", font=NORMAL).grid(row=0, column=0, padx=10, pady=10)
        self.firstname_entry = ctk.CTkEntry(firstname_frame)
        self.firstname_entry.grid(row=0, column=1, padx=10, pady=10)
        firstname_frame.pack(padx=10, pady=10)

        # Runner lastname entry
        lastname_frame = ctk.CTkFrame(parent)
        ctk.CTkLabel(lastname_frame, text="Last Name: ", font=NORMAL).grid(row=0, column=0, padx=10, pady=10)
        self.lastname_entry = ctk.CTkEntry(lastname_frame)
        self.lastname_entry.grid(row=0, column=1, padx=10, pady=10)
        lastname_frame.pack(padx=10, pady=10)

        # Runner age category entry
        age_cat_frame = ctk.CTkFrame(parent)
        ctk.CTkLabel(age_cat_frame)

        age_cat_frame.pack(padx=10, pady=10)