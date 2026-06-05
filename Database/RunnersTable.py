import pandas as pd

class RunnersTable:

    @staticmethod
    def create_table(conn):
        """Creates the 'runners' database table.
        """
        conn.execute("""
            CREATE TABLE IF NOT EXISTS runners (
            runner_id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            gender TEXT NOT NULL,
            age_category TEXT NOT NULL
            );""")
        conn.commit()
    
    @staticmethod
    def add_entry(conn, firstname:str, lastname:str, gender:str, age_category:str):
        """Adds a new runner into the 'runners' database table.
        """
        conn.execute("""
            INSERT OR REPLACE INTO runners 
            (firstname, lastname, gender, age_category)
            VALUES (?, ?, ?, ?)
            """, [firstname, lastname, gender, age_category])
        conn.commit()

    @staticmethod
    def get_all(db_conn):
        """Returns a dataframe of the 'runners' database table.

        Headings: (runner_id, firstname, lastname, gender, age_category)
        """
        runners = pd.read_sql("""
            SELECT * 
            FROM runners""", 
            db_conn)
        return runners
    
    @staticmethod
    def get(db_conn, runner_id:int):
        """Returns a specific runner from the 'runners' database table

        (firstname, lastname, gender, age_category)
        """
        runner = pd.read_sql(f"""
            SELECT firstname, lastname, gender, age_category
            FROM runners
            WHERE runner_id={runner_id}""", 
            db_conn).to_numpy()[0]
        return runner
