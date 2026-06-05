import pandas as pd
import json
from datetime import time

from Database.RacesTable import RacesTable
from Database.RunnersTable import RunnersTable
from config import *

class ResultsTable:

    @staticmethod
    def create_table(conn):
        """Creates the 'results' database table
        """
        conn.execute("""
            CREATE TABLE IF NOT EXISTS results (
                runner_id INTEGER NOT NULL,
                race_id INTEGER NOT NULL,
                result_time TIME,
                PRIMARY KEY (runner_id, race_id),
                FOREIGN KEY (runner_id) REFERENCES runners(runner_id) ON DELETE CASCADE,
                FOREIGN KEY (race_id) REFERENCES races(race_id) ON DELETE CASCADE   
            );""")
        conn.commit()
    
    @staticmethod
    def add_entry(conn, runner_id:int, race_id:int, result_time:time):
        """Adds a runner, race, time triple into the 'results' database table.
        """
        conn.execute("""
            INSERT OR REPLACE INTO race_results 
            (runner_id, race_id, time)
            VALUES (?, ?, ?)
            """, [runner_id, race_id, result_time])
        conn.commit()

    @staticmethod
    def get_all(db_conn) -> pd.DataFrame:
        """Returns a dataframe of the 'results' database table.

        Headings: (race_id, runner_id, result_time)
        """
        races = pd.read_sql("""
            SELECT * 
            FROM results""", 
            db_conn)
        return races
    
    @staticmethod
    def get(db_conn, runner_id:int, race_id:int) -> time:
        """Returns a specific result from the 'results' database table

        (result_time)
        """
        result_time = pd.read_sql(f"""
            SELECT result_time 
            FROM results
            WHERE runner_id={runner_id} AND race_id={race_id}""", 
            db_conn).to_numpy()[0]
        
        return time.strptime(result_time, TIME_FORMAT)
    
    def get_points(self, db_conn, runner_id:int, race_id:int) -> int:
        """Returns the number of points a result yields.
        """
        result_time = ResultsTable.get(db_conn, runner_id, race_id)
        name, distance, date, points = RacesTable.get(db_conn, race_id)
        firstname, lastname, gender, age_category = RunnersTable.get(db_conn, runner_id)

        if points is not None: return points
        
        standards = open("Standards.json")
        data = json.load(standards)
        standards.close()
        key = gender[0] + age_category
        standards = data[key][distance]

        points = 4
        for standard in standards:
            standard_time = time.strptime(standard, "")
            if result_time <= standard_time:
                points += 1
        if points == 9: points += 1
        return points
