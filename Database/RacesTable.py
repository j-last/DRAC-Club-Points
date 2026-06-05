import pandas as pd
from datetime import date

class RacesTable:

    @staticmethod
    def create_table(db_conn):
        """Creates the 'races' database table.
        """
        db_conn.execute("""
            CREATE TABLE IF NOT EXISTS races (
            race_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            distance TEXT NOT NULL,
            date DATE NOT NULL,
            points INTEGER
            );""")
        db_conn.commit()
    
    @staticmethod
    def add_entry(db_conn, name:str, distance:str, date:date, points:int|None):
        """Adds a new race into the 'races' database table.
        """
        db_conn.execute("""
            INSERT OR REPLACE INTO races 
            (name, distance, date, points)
            VALUES (?, ?, ?, ?)
            """, [name, distance, date, points])
        db_conn.commit()

    @staticmethod
    def get_all(db_conn):
        """Returns a dataframe of the 'races' database table.

        Headings: (race_id, name, distance, date, points)
        """
        races = pd.read_sql("""
            SELECT * 
            FROM races""", 
            db_conn)
        return races
    
    @staticmethod
    def get(db_conn, race_id:int):
        """Returns a specific race from the 'races' database table

        (name, distance, date, points)
        """
        race = pd.read_sql(f"""
            SELECT name, distance, date, points
            FROM races
            WHERE race_id={race_id};""", 
            db_conn).to_numpy()[0]
        return race
