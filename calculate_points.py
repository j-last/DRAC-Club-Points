import time
import json
import pandas as pd
from datetime import time
from GUI.gui_config import TIME_FORMAT

def calculate_points(runner_id:int, race_id:int, runner_time:time, db_conn) -> int:
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
        for standardTime in standards:
            if runner_time <= time.strptime(standardTime, TIME_FORMAT):
                points += 1
        if points == 9: points += 1
        return points


import sqlite3
conn = sqlite3.connect("Database/Club_100_2026.db")
conn.execute("PRAGMA foreign_keys = ON;")

race_results = pd.read_sql("SELECT * FROM race_results", conn).to_numpy()

for result in race_results:
    runner, race, runner_time = result
    runner_time = time.strptime(runner_time, TIME_FORMAT)
    print(calculate_points(runner, race, runner_time, conn))

conn.close()