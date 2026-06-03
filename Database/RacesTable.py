
class RacesTable:

    @staticmethod
    def create_table(conn):
        """Creates the 'races' database table.
        """
        conn.execute("""
            CREATE TABLE IF NOT EXISTS races (
            race_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            distance TEXT NOT NULL,
            date TEXT NOT NULL,
            fixed_points INTEGER
            );""")
        conn.commit()
    
    @staticmethod
    def add_entry(conn, name:str, distance:str, date, fixed_points:int|None):
        """Adds a new race into the 'races' database table.
        """
        conn.execute("""
            INSERT OR REPLACE INTO races 
            (name, distance, date, fixed_points)
            VALUES (?, ?, ?, ?)
            """, [name, distance, date, fixed_points])
        conn.commit()
