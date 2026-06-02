
class RunnersTable:

    @staticmethod
    def create_table(conn):
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
    def add_entry(conn, firstname, lastname, gender, age_category):
        conn.execute("""
            INSERT OR REPLACE INTO runners 
            (firstname, lastname, gender, age_category)
            VALUES (?, ?, ?, ?)
            """, [firstname, lastname, gender, age_category])
        conn.commit()
