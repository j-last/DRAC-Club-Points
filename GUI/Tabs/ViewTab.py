
from datetime import date

import customtkinter as ctk
import pandas as pd

from Database.RacesTable import RacesTable
from Database.RunnersTable import RunnersTable
from GUI.Tabs.RaceViewerTab import RaceViewerTab
from GUI.Tabs.RunnerViewerTab import RunnerViewerTab
from GUI.gui_helper_functions import Table
from config import *

from Database.ResultsTable import ResultsTable

class ViewTab:

    def __init__(self, parent, db_conn):
        """Sets up all elements within the 'View Race/Runner' tab
        """
        self.tabs = ctk.CTkTabview(parent)
        self.tabs._segmented_button.configure(font=HEADER2, fg_color="black")
        self.tabs.pack(expand=True, fill="both", padx=10, pady=10)

        self.tabs.add("View Race Results")
        self.race_viewer_tab = RaceViewerTab(self.tabs.tab("View Race Results"), db_conn)

        self.tabs.add("View Runner Results")
        self.runner_viewer_tab = RunnerViewerTab(self.tabs.tab("View Runner Results"), db_conn)
    
    def on_focus(self):
        self.race_viewer_tab.on_focus()
        self.runner_viewer_tab.on_focus()
