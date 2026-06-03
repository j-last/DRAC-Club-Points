
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
