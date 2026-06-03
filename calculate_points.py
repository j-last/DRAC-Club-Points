import time
import json
import pandas as pd

TIME_FORMAT = "%H.%M.%S"

def calculate_points(runner_id:int, race_id:int, runner_time, db_conn) -> int:
        """Calculates the number of points a runner should get for a race
        """
        distance, fixed_points = pd.read_sql(f"SELECT distance, fixed_points FROM races WHERE race_id={race_id}", db_conn).to_numpy()[0]

        if fixed_points is not None:
            return fixed_points
        
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

raceTime = time.strptime("00.21.22", TIME_FORMAT)
print(calculate_points(1, 1, raceTime, conn))

conn.close()