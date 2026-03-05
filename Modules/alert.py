import cv2
import os
import csv
import numpy as np
from datetime import datetime
import mediapipe as mp
import face_recognition
from ultralytics import YOLO

# ==========================================================
# LOAD MODELS
# ==========================================================

person_model = YOLO("yolov8s.pt")
weapon_model = YOLO(r"runs\detect\weapon_model\weights\best.pt")
face_model = YOLO("yolov8n-face.pt")

# ==========================================================
# MEDIAPIPE POSE SETUP
# ==========================================================

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# ==========================================================
# LOAD KNOWN FACES
# ==========================================================

known_face_encodings = []
known_face_names = []

if os.path.exists("known_faces"):
    for file in os.listdir("known_faces"):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join("known_faces", file)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                known_face_encodings.append(encodings[0])
                name = os.path.splitext(file)[0]
                known_face_names.append(name)

print("Loaded Known Faces:", known_face_names)

# ==========================================================
# GLOBAL MEMORY STRUCTURES
# ==========================================================

armed_ids = set()
identity_map = {}
alerted_ids = set()

# ==========================================================
# RISK ENGINE
# ==========================================================

def calculate_risk(armed, posture, identity):

    score = 0

    if armed:
        score += 5

    if identity == "Unknown":
        score += 2

    if posture == "HANDS UP":
        score += 3

    if posture == "FALLEN":
        score += 2

    if score >= 8:
        return "CRITICAL"
    elif score >= 5:
        return "HIGH"
    elif score >= 3:
        return "MEDIUM"
    else:
        return "LOW"

# ==========================================================
# EVENT LOGGER
# ==========================================================

log_file = "event_log.csv"

if not os.path.exists(log_file):
    with open(log_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Timestamp",
            "TrackID",
            "Name",
            "Posture",
            "Armed",
            "RiskLevel"
        ])

def log_event(track_id, name, posture, armed, risk):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            timestamp,
            track_id,
            name,
            posture,
            armed,
            risk
        ])

# ==========================================================
# POSTURE FUNCTION
# ==========================================================

def detect_posture(landmarks):

    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
    right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]

    shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
    hip_y = (left_hip.y + right_hip.y) / 2

    if abs(shoulder_y - hip_y) < 0.08:
        return "FALLEN"

    if left_wrist.y < left_shoulder.y and right_wrist.y < right_shoulder.y:
        return "HANDS UP"

    return "STANDING"

# ==========================================================
# VIDEO SETUP
# ==========================================================

video_path = "Prediction1.avi"
cap = cv2.VideoCapture(video_path)

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(
    "output_risk.mp4",
    fourcc,
    fps,
    (frame_width, frame_height)
)

print("Video Resolution:", frame_width, "x", frame_height)

# ==========================================================
# MAIN LOOP
# ==========================================================

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # PERSON TRACKING
    person_results = person_model.track(
        frame,
        persist=True,
        conf=0.4,
        classes=[0],
        verbose=False
    )

    # WEAPON DETECTION
    weapon_results = weapon_model(frame, conf=0.55, verbose=False)

    # FACE DETECTION
    face_results = face_model(frame, conf=0.2, verbose=False)

    persons = []
    weapons = []
    faces = []

    # Collect persons
    if person_results[0].boxes.id is not None:
        for box, track_id in zip(
                person_results[0].boxes.xyxy,
                person_results[0].boxes.id):

            x1, y1, x2, y2 = map(int, box)
            persons.append((int(track_id), x1, y1, x2, y2))

    # Collect weapons
    for box in weapon_results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        weapons.append((x1, y1, x2, y2))

    # Collect faces
    for box in face_results[0].boxes:
        fx1, fy1, fx2, fy2 = map(int, box.xyxy[0])
        faces.append((fx1, fy1, fx2, fy2))

    # Associate weapons to persons
    for wx1, wy1, wx2, wy2 in weapons:
        cx = (wx1 + wx2) // 2
        cy = (wy1 + wy2) // 2

        for track_id, px1, py1, px2, py2 in persons:
            if px1 <= cx <= px2 and py1 <= cy <= py2:
                armed_ids.add(track_id)

    # Draw weapons
    for wx1, wy1, wx2, wy2 in weapons:
        cv2.rectangle(frame, (wx1, wy1), (wx2, wy2),
                      (0, 255, 255), 2)
        cv2.putText(frame, "Weapon",
                    (wx1, wy1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 255), 2)

    # Process each person
    for track_id, px1, py1, px2, py2 in persons:

        person_roi = frame[max(py1, 0):min(py2, frame_height),
                           max(px1, 0):min(px2, frame_width)]

        # ================= FACE RECOGNITION =================
        if track_id not in identity_map:
            name = "Unknown"

            for fx1, fy1, fx2, fy2 in faces:
                if px1 <= fx1 <= px2 and py1 <= fy1 <= py2:

                    face_crop = frame[fy1:fy2, fx1:fx2]

                    if face_crop.size == 0:
                        continue

                    rgb_face = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
                    encodings = face_recognition.face_encodings(rgb_face)

                    if encodings:
                        face_encoding = encodings[0]

                        matches = face_recognition.compare_faces(
                            known_face_encodings,
                            face_encoding,
                            tolerance=0.6
                        )

                        face_distances = face_recognition.face_distance(
                            known_face_encodings,
                            face_encoding
                        )

                        if len(face_distances) > 0:
                            best_match_index = np.argmin(face_distances)
                            if matches[best_match_index]:
                                name = known_face_names[best_match_index]

            identity_map[track_id] = name
        else:
            name = identity_map[track_id]

        # ================= POSE DETECTION =================
        posture = "UNKNOWN"

        if person_roi.size > 0:
            roi_rgb = cv2.cvtColor(person_roi, cv2.COLOR_BGR2RGB)
            results = pose.process(roi_rgb)
            if results.pose_landmarks:
                posture = detect_posture(results.pose_landmarks.landmark)

        # ================= RISK ENGINE =================
        armed = track_id in armed_ids
        risk_level = calculate_risk(armed, posture, name)

        if risk_level in ["HIGH", "CRITICAL"] and track_id not in alerted_ids:
            print(f"⚠ ALERT: {risk_level} risk detected for ID {track_id} ({name})")
            log_event(track_id, name, posture, armed, risk_level)
            alerted_ids.add(track_id)

        # ================= COLOR BASED ON RISK =================
        if risk_level == "CRITICAL":
            color = (0, 0, 255)
        elif risk_level == "HIGH":
            color = (0, 165, 255)
        elif risk_level == "MEDIUM":
            color = (0, 255, 255)
        else:
            color = (0, 255, 0)

        # Draw person box
        cv2.rectangle(frame, (px1, py1), (px2, py2), color, 2)

        label = f"ID {track_id} | {name} | {posture} | {risk_level}"

        text_y = py1 - 10 if py1 > 20 else py1 + 25

        cv2.putText(frame, label,
                    (px1, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    2)

    out.write(frame)

    display_frame = cv2.resize(frame, (1000, 700))
    cv2.imshow("Smart AI Surveillance System", display_frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()