
import cv2
import time
import os
import sqlite3
from datetime import datetime

from app.detection.yolo_person import PersonDetector

# OUTPUT SETUP

OUTPUT_DIR = "Outputs/db_result"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Database path
DB_PATH = os.path.join(OUTPUT_DIR, "surveillance.db")

# Video output path
output_filename = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi"
output_path = os.path.join(OUTPUT_DIR, output_filename)


# DATABASE SETUP

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    person TEXT,
    status TEXT,
    posture TEXT,
    risk TEXT)""")
conn.commit()

def insert_event(timestamp, person, status, posture, risk):
    cursor.execute("""
        INSERT INTO events (timestamp, person, status, posture, risk)
        VALUES (?, ?, ?, ?, ?)
    """, (timestamp, person, status, posture, risk))
    conn.commit()


# INITIALIZE MODEL

MODEL_PATH = "models/yolov8s.pt"
detector = PersonDetector(MODEL_PATH)

VIDEO_PATH = "Sample_data/final_pipeline/Prediction.avi"
cap = cv2.VideoCapture(VIDEO_PATH)

# Video writer setup
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = int(cap.get(cv2.CAP_PROP_FPS))

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))


#  MEMORY FOR SMART LOGGING

previous_state = {}
last_logged_time = {}
COOLDOWN = 5

print("Running Video Test with DB + Output Saving...\n")


# 🎥 MAIN LOOP

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    persons = detector.detect(frame)

    for person in persons:
        person_id = person["id"]

        if person_id == -1:
            continue

        x1, y1, x2, y2 = map(int, person["bbox"])

        
        #  SIMULATED LOGIC
        
        weapon_detected = False
        posture = "STANDING"

        if person["confidence"] > 0.8:
            weapon_detected = True

        if (y2 - y1) < 100:
            posture = "FALLEN"

        
        #  EVENT LOGIC
        
        status = "ARMED" if weapon_detected else "SAFE"

        if weapon_detected:
            risk = "HIGH"
        elif posture == "FALLEN":
            risk = "MEDICAL"
        else:
            risk = "LOW"

        current_state = (status, posture)
        current_time = time.time()

        
        # 💾 SMART DATABASE LOGGING
        
        if (
            person_id not in previous_state or
            previous_state[person_id] != current_state
        ) and (
            current_time - last_logged_time.get(person_id, 0) > COOLDOWN):

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            insert_event(
                timestamp,
                f"ID_{person_id}",
                status,
                posture,
                risk )

            print(f" Logged: ID_{person_id} | {status} | {posture} | {risk}")

            previous_state[person_id] = current_state
            last_logged_time[person_id] = current_time

        
        # 🎥 DRAW OUTPUT
        
        color = (0, 0, 255) if status == "ARMED" else (0, 255, 0)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            frame,
            f"ID:{person_id} {status}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2 )

    # Save frame to video
    out.write(frame)

    # Display
    cv2.imshow("Smart Surveillance Test", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break


# CLEANUP

cap.release()
out.release()
conn.close()
cv2.destroyAllWindows()

print(f"\n Done! Outputs saved in: {OUTPUT_DIR}")