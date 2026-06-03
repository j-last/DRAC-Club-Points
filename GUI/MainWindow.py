import customtkinter as ctk

from GUI.gui_config import HEADER1

from GUI.Tabs.ManualEntryTab import ManualEntryTab
from GUI.Tabs.CreateRaceTab import CreateRaceTab
from GUI.Tabs.CreateRunnerTab import CreateRunnerTab
from GUI.Tabs.RacesTab import RacesTab


class MainWindow:

    def __init__(self, db_conn):

        self.root = ctk.CTk()
        self.root.title("DRAC Club Points")
        self.root.geometry("1280x720")

        self.tabs = ctk.CTkTabview(self.root)
        self.tabs._segmented_button.configure(font=HEADER1)
        self.tabs.configure(command=self.tab_changed)
        self.tabs.pack(expand=True, fill="both", padx=10, pady=10)

        self.tabs.add("Manual Entry")
        self.manual_entry_tab = ManualEntryTab(self.tabs.tab("Manual Entry"), db_conn)

        self.tabs.add("Create Race")
        self.create_race_tab = CreateRaceTab(self.tabs.tab("Create Race"), db_conn)

        self.tabs.add("Create Runner")
        self.create_runner_tab = CreateRunnerTab(self.tabs.tab("Create Runner"), db_conn)

        self.tabs.add("Race Viewer")
        self.races_tab = RacesTab(self.tabs.tab("Race Viewer"), db_conn)
        

    def tab_changed(self):
        tab = self.tabs.get()

        if tab == "Manual Entry":
            self.manual_entry_tab.on_focus()