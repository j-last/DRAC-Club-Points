from GUI.MainWindow import MainWindow

import sqlite3

conn = sqlite3.connect("Database/Club_100_2026.db")
conn.execute("PRAGMA foreign_keys = ON;")

MainWindow(conn).root.mainloop()

conn.close()
