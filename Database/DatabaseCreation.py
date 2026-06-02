
import sqlite3

db_filename = "Club_100_2026.db"

conn = sqlite3.connect(db_filename)
conn.execute("PRAGMA foreign_keys = ON;")



conn.close()