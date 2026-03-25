import cv2
import os
import mediapipe as mp
from ultralytics import YOLO
from mediapipe.python.solutions import pose

# Load Models

person_model_path = os.path.join("..", "Models", "yolov8s.pt")
person_model = YOLO(person_model_path)

weapon_model_path = os.path.join("..", "runs", "detect", "weapon_model", "weights", "best.pt")
weapon_model = YOLO(weapon_model_path)


# Initialize MediaPipe Pose

mp_pose = pose

pose_detector = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)


# Video Input

video_path = os.path.join("..", "testing_samples", "Prediction1.avi")
cap = cv2.VideoCapture(video_path)


# Output Directory Setup

output_dir = os.path.abspath(os.path.join("..", "Output_samples", "pose_detection"))

os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "output_pose.mp4")


# Get Video Properties

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Video Writer

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

out = cv2.VideoWriter(
    output_path,
    fourcc,
    fps,
    (frame_width, frame_height))


# Display Window

cv2.namedWindow("AI Smart Surveillance System", cv2.WINDOW_NORMAL)
cv2.resizeWindow("AI Smart Surveillance System", 1000, 700)


# Data Storage

armed_ids = set()


# Posture Detection Function

def detect_posture(landmarks):

    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]  # x, y, z
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]

    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
    right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]

    shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
    hip_y = (left_hip.y + right_hip.y) / 2

    # Fallen detection
    if abs(shoulder_y - hip_y) < 0.08:
        return "FALLEN"

    # Hands up detection
    if left_wrist.y < left_shoulder.y and right_wrist.y < right_shoulder.y:
        return "HANDS UP"

    return "STANDING"


# Main Processing Loop

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # models

    person_results = person_model.track( frame, persist=True, conf=0.4, classes=[0], verbose=False )

    weapon_results = weapon_model( frame, conf=0.55, verbose=False )


    persons = []
    weapons = []


    # Collect Person Boxes

    if person_results[0].boxes.id is not None:

        for box, track_id in zip(
                person_results[0].boxes.xyxy,
                person_results[0].boxes.id):

            x1, y1, x2, y2 = map(int, box)
            track_id = int(track_id)

            persons.append((track_id, x1, y1, x2, y2))


    # Collect Weapon Boxes

    for box in weapon_results[0].boxes:

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        weapons.append((x1, y1, x2, y2))


    # ==============================
    # Associate Weapons With Persons
    # ==============================

    for wx1, wy1, wx2, wy2 in weapons:

        cx = (wx1 + wx2) // 2
        cy = (wy1 + wy2) // 2

        for track_id, px1, py1, px2, py2 in persons:

            if px1 <= cx <= px2 and py1 <= cy <= py2:
                armed_ids.add(track_id)


    # ==============================
    # Draw Weapon Boxes
    # ==============================

    for wx1, wy1, wx2, wy2 in weapons:

        cv2.rectangle(frame, (wx1, wy1), (wx2, wy2), (0, 255, 255), 2)

        cv2.putText(
            frame,
            "Weapon",
            (wx1, wy1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2
        )


    # ==============================
    # Process Each Person
    # ==============================

    for track_id, px1, py1, px2, py2 in persons:

        person_roi = frame[py1:py2, px1:px2]

        posture = "UNKNOWN"

        if person_roi.size > 0:

            roi_rgb = cv2.cvtColor(person_roi, cv2.COLOR_BGR2RGB)
            results = pose_detector.process(roi_rgb)

            if results.pose_landmarks:
                posture = detect_posture(results.pose_landmarks.landmark)


        # Color logic
        if track_id in armed_ids:
            color = (0, 0, 255)   # Red
        else:
            color = (0, 255, 0)   # Green


        cv2.rectangle(frame, (px1, py1), (px2, py2), color, 2)

        label = f"ID {track_id} | {posture}"

        cv2.putText(
            frame,
            label,
            (px1, py1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )


    # ==============================
    # Save Frame
    # ==============================

    out.write(frame)


    # ==============================
    # Display Frame
    # ==============================

    cv2.imshow("AI Smart Surveillance System", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break


# ==============================
# Release Resources
# ==============================

cap.release()
out.release()
cv2.destroyAllWindows()