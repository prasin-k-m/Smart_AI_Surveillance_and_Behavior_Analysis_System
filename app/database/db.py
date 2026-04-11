
import sqlite3
import time

# CONNECTION 
DB_PATH = "surveillance.db"


def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


# CREATE / UPDATE TABLE 
def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create table (if not exists)
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

    #  ADD NEW COLUMN SAFELY 

    conn.close()


# TRACKING MEMORY (NEW)
last_saved_time = {}   # track_id → last saved timestamp
COOLDOWN = 5           # seconds


# INSERT FUNCTION 
def insert_event(timestamp, person, status, posture, risk):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO events (timestamp, person, status, posture, risk)
        VALUES (?, ?, ?, ?, ?)
    """, (
        timestamp,
        person,
        status,
        posture,
        risk
    ))

    conn.commit()
    conn.close()


#  SMART INSERT (NO DUPLICATES) 
def smart_insert(track_id, timestamp, status, posture, risk):
    global last_saved_time

    # Skip invalid IDs
    if track_id == -1:
        return

    current_time = time.time()

    # First time seeing this person
    if track_id not in last_saved_time:
        insert_event(
            timestamp,
            f"Person_{track_id}",
            status,
            posture,
            risk
        )
        last_saved_time[track_id] = current_time
        return

    # Cooldown logic
    last_time = last_saved_time.get(track_id, 0)

    if current_time - last_time > COOLDOWN:
        insert_event(
            timestamp,
            f"Person_{track_id}",
            status,
            posture,
            risk
        )
        last_saved_time[track_id] = current_time


# FETCH ALL EVENTS 
def fetch_all_events(limit=50):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM events
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return rows


# FETCH BY FILTER 
def fetch_by_filter(column, value):
    conn = get_connection()
    cursor = conn.cursor()

    query = f"SELECT * FROM events WHERE {column}=? ORDER BY id DESC LIMIT 20"
    cursor.execute(query, (value,))

    rows = cursor.fetchall()
    conn.close()

    return rows


# INIT CALL 
initialize_db()

