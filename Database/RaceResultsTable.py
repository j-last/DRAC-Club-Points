
class RaceResultsTable:

    @staticmethod
    def create_table(conn):
        conn.execute("""
            CREATE TABLE IF NOT EXISTS race_results (
                runner_id INTEGER NOT NULL,
                race_id INTEGER NOT NULL,
                runner_time TIME,
                PRIMARY KEY (runner_id, race_id),
                FOREIGN KEY (runner_id) REFERENCES runners(runner_id) ON DELETE CASCADE,
                FOREIGN KEY (race_id) REFERENCES races(race_id) ON DELETE CASCADE   
            );""")
        conn.commit()
    
    @staticmethod
    def add_entry(conn, runner_id, race_id, runner_time):
        conn.execute("""
            INSERT OR REPLACE INTO race_results 
            (runner_id, race_id, runner_time)
            VALUES (?, ?, ?, ?)
            """, [runner_id, race_id, runner_time])
        conn.commit()