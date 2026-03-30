import cv2
import time
from datetime import datetime

from app.detection.yolo_person import PersonDetector
from app.database.db import insert_event

# -------------------------------
# 🔧 INITIALIZE
# -------------------------------


MODEL_PATH = "models/yolov8s.pt"
detector = PersonDetector(MODEL_PATH)

# Use your video file here

VIDEO_PATH = "Sample_data/final_pipeline/Prediction.avi"
cap = cv2.VideoCapture(VIDEO_PATH)

# Memory for smart logging
previous_state = {}
last_logged_time = {}
COOLDOWN = 5  # seconds

print("🚀 Running Video Test with DB Logging...\n")

# -------------------------------
# 🎥 MAIN LOOP
# -------------------------------
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    persons = detector.detect(frame)

    for person in persons:
        person_id = person["id"]

        # Skip invalid tracking IDs
        if person_id == -1:
            continue

        x1, y1, x2, y2 = map(int, person["bbox"])

        # -------------------------------
        # 🧠 SIMULATED LOGIC (REPLACE LATER)
        # -------------------------------
        weapon_detected = False
        posture = "STANDING"

        # Example condition
        if person["confidence"] > 0.8:
            weapon_detected = True

        # If bounding box height is small → fallen
        if (y2 - y1) < 100:
            posture = "FALLEN"

        # -------------------------------
        # 🎯 EVENT LOGIC
        # -------------------------------
        status = "ARMED" if weapon_detected else "SAFE"

        if weapon_detected:
            risk = "HIGH"
        elif posture == "FALLEN":
            risk = "MEDICAL"
        else:
            risk = "LOW"

        current_state = (status, posture)
        current_time = time.time()

        # -------------------------------
        # 💾 SMART DATABASE LOGGING
        # -------------------------------
        if (
            person_id not in previous_state or
            previous_state[person_id] != current_state
        ) and (
            current_time - last_logged_time.get(person_id, 0) > COOLDOWN
        ):

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            insert_event(
                timestamp,
                f"ID_{person_id}",
                status,
                posture,
                risk
            )

            print(f"✅ Logged: ID_{person_id} | {status} | {posture} | {risk}")

            previous_state[person_id] = current_state
            last_logged_time[person_id] = current_time

        # -------------------------------
        # 🎥 DRAW OUTPUT
        # -------------------------------
        color = (0, 0, 255) if status == "ARMED" else (0, 255, 0)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            frame,
            f"ID:{person_id} {status}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

    # -------------------------------
    # 🖥️ DISPLAY
    # -------------------------------
    cv2.imshow("Smart Surveillance Test", frame)

    # Press ESC to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

# -------------------------------
# 🧹 CLEANUP
# -------------------------------
cap.release()
cv2.destroyAllWindows()

print("\n🎉 Test Completed Successfully!")