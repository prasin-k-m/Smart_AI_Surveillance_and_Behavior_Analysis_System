import sqlite3

conn = sqlite3.connect("surveillance.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    person TEXT,
    status TEXT,
    posture TEXT,
    risk TEXT
)
""")

conn.commit()


def insert_event(timestamp, person, status, posture, risk):
    cursor.execute("""
        INSERT INTO events (timestamp, person, status, posture, risk)
        VALUES (?, ?, ?, ?, ?)
    """, (timestamp, person, status, posture, risk))

    conn.commit()