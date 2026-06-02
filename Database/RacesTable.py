
class RacesTable:

    @staticmethod
    def create_table(conn):
        conn.execute("""
            CREATE TABLE IF NOT EXISTS races (
            race_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            distance TEXT,
            date DATE,
            fixed_points INTEGER
            );""")
        conn.commit()
    
    @staticmethod
    def add_entry(conn, name, distance, date, fixed_points):
        conn.execute("""
            INSERT OR REPLACE INTO races 
            (name, distance, date, fixed_points)
            VALUES (?, ?, ?, ?)
            """, [name, distance, date, fixed_points])
        conn.commit()
