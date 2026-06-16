import customtkinter as ctk

from GUI.Tabs.ManualEntryTab import ManualEntryTab
from GUI.Tabs.CreateTab import CreateTab
from GUI.Tabs.ViewTab import ViewTab
from GUI.Tabs.TotalsTab import TotalsTab
from GUI.Tabs.UrlEntryTab import UrlEntryTab

from config import *

class MainWindow:

    def __init__(self, db_conn):
        """Sets up the window and tabs for the GUI
        """

        self.root = ctk.CTk()
        self.root.title("DRAC Club Points")
        self.root.geometry("1280x720")

        self.tabs = ctk.CTkTabview(self.root)
        self.tabs._segmented_button.configure(font=HEADER1, fg_color="black")
        self.tabs.configure(command=self.tab_changed)
        self.tabs.pack(expand=True, fill="both", padx=10, pady=10)

        self.tabs.add("Manual Entry")
        self.manual_entry_tab = ManualEntryTab(self.tabs.tab("Manual Entry"), db_conn)

        self.tabs.add("Create Race/Runner")
        self.create_tab = CreateTab(self.tabs.tab("Create Race/Runner"), db_conn)

        self.tabs.add("View Race/Runner")
        self.view_tab = ViewTab(self.tabs.tab("View Race/Runner"), db_conn)

        self.tabs.add("Total Points/Parkruns")
        self.totals_tab = TotalsTab(self.tabs.tab("Total Points/Parkruns"), db_conn)

        self.tabs.add("Race URL")
        self.total_race_timing_tab = UrlEntryTab(self.tabs.tab("Race URL"), db_conn)
        

    def tab_changed(self):
        """Ran when the tab is changed by the user.
        Updates UI elements that need updating when each tab is brought into focus.
        """
        tab = self.tabs.get()

        if tab == "Manual Entry":
            self.manual_entry_tab.on_focus()
        elif tab == "View Race/Runner":
            self.view_tab.on_focus()
        elif tab == "Total Points/Parkruns":
            self.totals_tab.on_focus()
        elif tab == "Race URL":
            self.total_race_timing_tab.on_focus()
