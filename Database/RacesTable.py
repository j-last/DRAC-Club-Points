
class RacesTable:

    @staticmethod
    def create_table(conn):
        conn.execute("""
            CREATE TABLE IF NOT EXISTS races (
            race_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            distance TEXT,
            date DATE,
            fixedPoints INTEGER
            );""")
        conn.commit()
    
    @staticmethod
    def add_entry(conn, name, distance, date, fixedPoints):
        conn.execute("""
            INSERT OR REPLACE INTO races 
            (name, distance, date, fixedPoints)
            VALUES (?, ?, ?, ?)
            """, name, distance, date, fixedPoints)
        conn.commit()
