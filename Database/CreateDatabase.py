import sqlite3

from RunnersTable import RunnersTable
from RacesTable import RacesTable
from RaceResultsTable import RaceResultsTable

def create_database(db_filename):
    conn = sqlite3.connect(db_filename)
    conn.execute("PRAGMA foreign_keys = ON;")

    RunnersTable.create_table(conn)
    RacesTable.create_table(conn)
    RaceResultsTable.create_table(conn)

    conn.close()

# Commented out for accidental run protection
# create_database("Database/Club_100_2026.db")
