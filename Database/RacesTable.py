import pandas as pd
from datetime import date
from config import *

class RacesTable:

    @staticmethod
    def create_table(db_conn):
        """Creates the 'races' database table.
        """
        db_conn.execute("""
            CREATE TABLE IF NOT EXISTS races (
            race_id INTEGER PRIMARY KEY AUTOINCREMENT,
            race_name TEXT NOT NULL,
            race_distance TEXT NOT NULL,
            race_date DATE NOT NULL,
            race_points INTEGER
            );""")
        db_conn.commit()
    
    @staticmethod
    def add_entry(db_conn, race_name:str, race_distance:str, race_date:date, race_points:int|None):
        """Adds a new race into the 'races' database table.

        If a race with that name already exists then the values for that race are updated.
        """
        if race_name == "parkrun": race_points = 0
        date_str = race_date.strftime(DATE_FORMAT_DATABASE)
        if RacesTable.race_exists(db_conn, race_name):
            db_conn.execute("""
                UPDATE races
                SET race_distance = ?, race_date = ?, race_points = ?
                WHERE race_name = ?;
                """, (race_distance, race_date, race_points, race_name))
            db_conn.commit()
        else:
            db_conn.execute("""
                INSERT OR REPLACE INTO races 
                (race_name, race_distance, race_date, race_points)
                VALUES (?, ?, ?, ?)
                """, [race_name, race_distance, date_str, race_points])
            db_conn.commit()
        

    @staticmethod
    def get_all(db_conn):
        """Returns a dataframe of the 'races' database table.

        Headings: (race_id, race_name, race_distance, race_date, race_points)
        """
        races = pd.read_sql("""
            SELECT * 
            FROM races""", 
            db_conn)
        races['race_date'] = pd.to_datetime(races['race_date'], format=DATE_FORMAT_DATABASE)
        return races
    
    @staticmethod
    def get(db_conn, race_id:int):
        """Returns a specific race from the 'races' database table

        (race_name, race_distance, race_date, race_points)
        """
        race = pd.read_sql(f"""
            SELECT race_name, race_distance, race_date, race_points
            FROM races
            WHERE race_id={race_id};""", 
            db_conn)
        race['race_date'] = pd.to_datetime(race['race_date'], format=DATE_FORMAT_DATABASE)
        return race.to_numpy()[0]
    
    @staticmethod
    def get_all_by_runner(db_conn, runner_id:int):
        """Returns a dataframe of all races by a specific runner.
        
        (race_id, race_name, race_distance, race_date, race_points, result_time)
        """
        races = pd.read_sql(f"""
                    SELECT races.race_id, race_name, race_distance, race_date, race_points, result_time
                    FROM races
                    JOIN results ON races.race_id = results.race_id
                    WHERE runner_id = {runner_id}
                    """, db_conn)
        races['race_date'] = pd.to_datetime(races['race_date'], format=DATE_FORMAT_DATABASE)
        races['result_time'] = pd.to_datetime(races['result_time'], format=TIME_FORMAT, errors="coerce")
        return races
    
    @staticmethod
    def race_exists(db_conn, race_name:str) -> bool:
        """Returns True if a race with that name already exists, otherwise False.
        """
        if race_name == "parkrun": return False
        races = pd.read_sql(f"""
            SELECT *
            FROM races
            WHERE race_name = '{race_name}'
            """, db_conn)
        
        if len(races) > 0:
            return True
        else:
            return False
        

        
