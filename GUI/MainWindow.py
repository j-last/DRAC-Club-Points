import customtkinter as ctk

from GUI.gui_config import HEADER1

from GUI.Tabs.ManualEntryTab import ManualEntryTab
from GUI.Tabs.CreateRaceTab import CreateRaceTab
from GUI.Tabs.CreateRunnerTab import CreateRunnerTab
from GUI.Tabs.RaceViewerTab import RaceViewerTab
from GUI.Tabs.RunnerViewerTab import RunnerViewerTab
from GUI.Tabs.PointsTotalsTab import PointsTotalsTab
from GUI.Tabs.ParkrunsTotalTab import ParkrunsTotalsTab

class MainWindow:

    def __init__(self, db_conn):
        """Sets up the window and tabs for the GUI
        """

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
        self.race_viewer_tab = RaceViewerTab(self.tabs.tab("Race Viewer"), db_conn)

        self.tabs.add("Runner Viewer")
        self.runner_viewer_tab = RunnerViewerTab(self.tabs.tab("Runner Viewer"), db_conn)

        self.tabs.add("Points Totals")
        self.points_totals_tab = PointsTotalsTab(self.tabs.tab("Points Totals"), db_conn)

        self.tabs.add("Parkruns Totals")
        self.parkruns_totals_tab = ParkrunsTotalsTab(self.tabs.tab("Parkruns Totals"), db_conn)
        

    def tab_changed(self):
        """Ran when the tab is changed by the user.
        Updates UI elements that need updating when each tab is brought into focus.
        """
        tab = self.tabs.get()

        if tab == "Manual Entry":
            self.manual_entry_tab.on_focus()
        elif tab == "Race Viewer":
            self.race_viewer_tab.on_focus()
        elif tab == "Runner Viewer":
            self.runner_viewer_tab.on_focus()
        elif tab == "Points Totals":
            self.points_totals_tab.on_focus()
        elif tab == "Parkruns Totals":
            self.parkruns_totals_tab.on_focus()
