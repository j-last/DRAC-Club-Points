import customtkinter as ctk

from ManualEntryTab import ManualEntryTab
from CreateRunnerTab import CreateRunnerTab

HEADER1 = ("Helvetica", 20, "bold")
HEADER2 = ("Helvetica", 18, "bold")
HEADER3 = ("Helvetica", 16, "bold")
NORMAL = ("Helvetica", 14)

class MainWindow:

    def __init__(self):

        self.root = ctk.CTk()
        self.root.title("DRAC Club Points")
        self.root.geometry("1280x720")

        self.tabs = ctk.CTkTabview(self.root)
        self.tabs._segmented_button.configure(font=HEADER1)
        self.tabs.pack(expand=True, fill="both", padx=10, pady=10)

        self.tabs.add("Manual Entry")
        ManualEntryTab(self.tabs.tab("Manual Entry"))

        self.tabs.add("Create Runner")
        CreateRunnerTab(self.tabs.tab("Create Runner"))


MainWindow().root.mainloop()

