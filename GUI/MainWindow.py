import customtkinter as ctk

from gui_config import HEADER1

from Tabs.CreateRaceTab import CreateRaceTab
from Tabs.ManualEntryTab import ManualEntryTab
from Tabs.CreateRunnerTab import CreateRunnerTab


class MainWindow:

    def __init__(self):

        self.root = ctk.CTk()
        self.root.title("DRAC Club Points")
        self.root.geometry("1280x720")

        self.tabs = ctk.CTkTabview(self.root)
        self.tabs._segmented_button.configure(font=HEADER1)
        self.tabs.pack(expand=True, fill="both", padx=10, pady=10)

        self.tabs.add("Create Race")
        CreateRaceTab(self.tabs.tab("Create Race"))

        self.tabs.add("Manual Entry")
        ManualEntryTab(self.tabs.tab("Manual Entry"))

        self.tabs.add("Create Runner")
        CreateRunnerTab(self.tabs.tab("Create Runner"))


MainWindow().root.mainloop()

