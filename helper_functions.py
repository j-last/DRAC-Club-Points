import time
import json
import pandas as pd
from datetime import time
from GUI.gui_config import TIME_FORMAT
import requests
from bs4 import BeautifulSoup as bs

def calculate_points(runner_id:int, race_id:int, runner_time:str, db_conn) -> int:
        """Calculates the number of points a runner should get for a race
        """
        distance, fixed_points = pd.read_sql(f"SELECT distance, fixed_points FROM races WHERE race_id={race_id}", db_conn).to_numpy()[0]

        if fixed_points is not None:
            return int(fixed_points)
        
        gender, age_cat = pd.read_sql(f"SELECT gender, age_category FROM runners WHERE runner_id={runner_id}", db_conn).to_numpy()[0]

        standards = open("Standards.json")
        data = json.load(standards)
        standards.close()

        key = gender[0] + age_cat
        standards = data[key][distance]

        points = 4
        runner_time_object = time.strptime(runner_time, TIME_FORMAT)
        for standardTime in standards:
            if runner_time_object <= time.strptime(standardTime, TIME_FORMAT):
                points += 1
        if points == 9: points += 1
        return points

"""
import sqlite3
conn = sqlite3.connect("Database/Club_100_2026.db")
conn.execute("PRAGMA foreign_keys = ON;")

race_results = pd.read_sql("SELECT * FROM race_results", conn).to_numpy()

for result in race_results:
    runner, race, runner_time = result
    print(calculate_points(runner, race, runner_time, conn))

conn.close()
"""

def get_total_race_timings_results(url:str) -> dict[str:time]:
    """Web scrapes all dereham runners AC results from a totalracetiming website.
    Returns a dictionary with entries in the form {runnerName : runnerTime}
    """
    race_runners = {}

    page = requests.get(url)
    soup = bs(page.content, "html.parser")
    runners = soup.find("tbody") # gets all 

    for runner in runners:
        runnerstring = runner.decode_contents()
        if "<td>Dereham Runners AC</td>" in runnerstring:
            runnerstring = runnerstring.split("<td")
            name = (runnerstring[2][1:-5] + " " + runnerstring[3][1:-5]).upper()
            raceTime = time.strptime(runnerstring[-2][2:-8], "%H:%M:%S")

            race_runners[name] = raceTime
    
    return race_runners