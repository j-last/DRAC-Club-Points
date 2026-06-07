import pandas as pd
from config import *

class RunnersTable:

    @staticmethod
    def create_table(conn):
        """Creates the 'runners' database table.
        """
        conn.execute("""
            CREATE TABLE IF NOT EXISTS runners (
            runner_id INTEGER PRIMARY KEY AUTOINCREMENT,
            runner_firstname TEXT NOT NULL,
            runner_lastname TEXT NOT NULL,
            runner_gender TEXT NOT NULL,
            runner_age_category TEXT NOT NULL
            );""")
        conn.commit()
    
    @staticmethod
    def add_entry(db_conn, runner_firstname:str, runner_lastname:str, runner_gender:str, runner_age_category:str):
        """Adds a new runner into the 'runners' database table.

        If a runner with that name already exists, the values are updated.
        """
        if RunnersTable.runner_exists(db_conn, runner_firstname, runner_lastname):
            db_conn.execute(f"""
                UPDATE runners
                SET runner_gender = '{runner_gender}', runner_age_category = '{runner_age_category}'
                WHERE runner_firstname = '{runner_firstname}' AND runner_lastname = '{runner_lastname}';
                """)
            db_conn.commit()
        else:
            db_conn.execute("""
                INSERT OR REPLACE INTO runners 
                (runner_firstname, runner_lastname, runner_gender, runner_age_category)
                VALUES (?, ?, ?, ?)
                """, [runner_firstname, runner_lastname, runner_gender, runner_age_category])
            db_conn.commit()

    @staticmethod
    def get_all(db_conn):
        """Returns a dataframe of the 'runners' database table.

        Headings: (runner_id, runner_firstname, runner_lastname, runner_gender, runner_age_category)
        """
        runners = pd.read_sql("""
            SELECT * 
            FROM runners""", 
            db_conn)
        return runners
    
    @staticmethod
    def get(db_conn, runner_id:int):
        """Returns a specific runner from the 'runners' database table

        (runner_firstname, runner_lastname, runner_gender, runner_age_category)
        """
        runner = pd.read_sql(f"""
            SELECT runner_firstname, runner_lastname, runner_gender, runner_age_category
            FROM runners
            WHERE runner_id={runner_id}""", 
            db_conn).to_numpy()[0]
        return runner
    
    @staticmethod
    def get_all_by_race(db_conn, race_id):
        """Returns a dataframe of all runners who competed in a specific race.

        Headings: (runner_id, runner_firstname, runner_lastname, runner_gender, runner_age_category, result_time)
        """
        runners = pd.read_sql(f"""
            SELECT runners.runner_id, runner_firstname, runner_lastname, runner_gender, runner_age_category, result_time
            FROM runners
            JOIN results ON results.runner_id = runners.runner_id
            WHERE results.race_id = {race_id}
            """, db_conn)
        runners['result_time'] = pd.to_datetime(runners['result_time'], format=TIME_FORMAT, errors="coerce")
        return runners
    
    @staticmethod
    def runner_exists(db_conn, runner_firstname:str, runner_lastname:str) -> bool:
        """Returns True if a runner with that name already exists, otherwise False.
        """
        races = pd.read_sql(f"""
            SELECT *
            FROM runners
            WHERE runner_firstname = '{runner_firstname}' AND runner_lastname = '{runner_lastname}';
            """, db_conn)
        
        if len(races) > 0:
            return True
        else:
            return False
