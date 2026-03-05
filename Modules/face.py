# import cv2
# import os
# import numpy as np
# import mediapipe as mp
# import face_recognition
# from ultralytics import YOLO

# # ==========================================================
# # LOAD MODELS
# # ==========================================================

# # Person detection model
# person_model = YOLO("yolov8s.pt")

# # Custom weapon detection model
# weapon_model = YOLO(r"runs\detect\weapon_model\weights\best.pt")

# # Face detection model (IMPORTANT)
# face_model = YOLO("yolov8n-face.pt")

# # MediaPipe Pose
# mp_pose = mp.solutions.pose
# pose = mp_pose.Pose(
#     static_image_mode=False,
#     model_complexity=1,
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5
# )

# # ==========================================================
# # LOAD KNOWN FACES
# # ==========================================================

# known_face_encodings = []
# known_face_names = []

# for file in os.listdir("known_faces"):

#     if file.lower().endswith((".jpg", ".jpeg", ".png")):
#         image_path = os.path.join("known_faces", file)
#         image = face_recognition.load_image_file(image_path)
#         encodings = face_recognition.face_encodings(image)

#         if encodings:
#             known_face_encodings.append(encodings[0])
#             name = os.path.splitext(file)[0]
#             known_face_names.append(name)

# print("Loaded Known Faces:", known_face_names)

# # ==========================================================
# # HELPER STRUCTURES
# # ==========================================================

# armed_ids = set()
# identity_map = {}

# # ==========================================================
# # POSTURE FUNCTION
# # ==========================================================

# def detect_posture(landmarks):

#     left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
#     right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
#     left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
#     right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
#     left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
#     right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]

#     shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
#     hip_y = (left_hip.y + right_hip.y) / 2

#     if abs(shoulder_y - hip_y) < 0.08:
#         return "FALLEN"

#     if left_wrist.y < left_shoulder.y and right_wrist.y < right_shoulder.y:
#         return "HANDS UP"

#     return "STANDING"

# # ==========================================================
# # VIDEO SETUP
# # ==========================================================

# video_path = "Prediction1.avi"
# cap = cv2.VideoCapture(video_path)

# frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fps = cap.get(cv2.CAP_PROP_FPS)

# fourcc = cv2.VideoWriter_fourcc(*"mp4v")
# out = cv2.VideoWriter(
#     "output_face.mp4",
#     fourcc,
#     fps,
#     (frame_width, frame_height)
# )

# # ==========================================================
# # MAIN LOOP
# # ==========================================================

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # -------------------------------
#     # PERSON TRACKING
#     # -------------------------------
#     person_results = person_model.track(
#         frame,
#         persist=True,
#         conf=0.4,
#         classes=[0],
#         verbose=False
#     )

#     # -------------------------------
#     # WEAPON DETECTION
#     # -------------------------------
#     weapon_results = weapon_model(frame, conf=0.55, verbose=False)

#     # -------------------------------
#     # FACE DETECTION (FULL FRAME)
#     # -------------------------------
#     face_results = face_model(frame, conf=0.5, verbose=False)

#     persons = []
#     weapons = []
#     faces = []

#     # Collect persons
#     if person_results[0].boxes.id is not None:
#         for box, track_id in zip(
#                 person_results[0].boxes.xyxy,
#                 person_results[0].boxes.id):

#             x1, y1, x2, y2 = map(int, box)
#             track_id = int(track_id)
#             persons.append((track_id, x1, y1, x2, y2))

#     # Collect weapons
#     for box in weapon_results[0].boxes:
#         x1, y1, x2, y2 = map(int, box.xyxy[0])
#         weapons.append((x1, y1, x2, y2))

#     # Collect faces
#     for box in face_results[0].boxes:
#         fx1, fy1, fx2, fy2 = map(int, box.xyxy[0])
#         faces.append((fx1, fy1, fx2, fy2))

#     # -------------------------------
#     # ASSOCIATE WEAPON TO PERSON
#     # -------------------------------
#     for wx1, wy1, wx2, wy2 in weapons:
#         cx = (wx1 + wx2) // 2
#         cy = (wy1 + wy2) // 2

#         for track_id, px1, py1, px2, py2 in persons:
#             if px1 <= cx <= px2 and py1 <= cy <= py2:
#                 armed_ids.add(track_id)

#     # -------------------------------
#     # PROCESS EACH PERSON
#     # -------------------------------
#     for track_id, px1, py1, px2, py2 in persons:

#         person_roi = frame[py1:py2, px1:px2]

#         # ===============================
#         # FACE RECOGNITION USING YOLO FACE
#         # ===============================

#         if track_id not in identity_map:
#             name = "Unknown"

#             for fx1, fy1, fx2, fy2 in faces:

#                 # Check if face is inside person box
#                 if px1 <= fx1 <= px2 and py1 <= fy1 <= py2:

#                     face_crop = frame[fy1:fy2, fx1:fx2]

#                     if face_crop.size == 0:
#                         continue

#                     rgb_face = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
#                     encodings = face_recognition.face_encodings(rgb_face)

#                     if encodings:
#                         face_encoding = encodings[0]

#                         matches = face_recognition.compare_faces(
#                             known_face_encodings, face_encoding)

#                         face_distances = face_recognition.face_distance(
#                             known_face_encodings, face_encoding)

#                         if len(face_distances) > 0:
#                             best_match_index = np.argmin(face_distances)

#                             if matches[best_match_index]:
#                                 name = known_face_names[best_match_index]

#             identity_map[track_id] = name
#         else:
#             name = identity_map[track_id]

#         # ===============================
#         # POSE DETECTION
#         # ===============================

#         posture = "UNKNOWN"

#         if person_roi.size > 0:
#             roi_rgb = cv2.cvtColor(person_roi, cv2.COLOR_BGR2RGB)
#             results = pose.process(roi_rgb)

#             if results.pose_landmarks:
#                 posture = detect_posture(results.pose_landmarks.landmark)

#         # ===============================
#         # COLOR LOGIC
#         # ===============================

#         if track_id in armed_ids:
#             color = (0, 0, 255)
#             status = "ARMED"
#         else:
#             color = (0, 255, 0)
#             status = "NORMAL"

#         # ===============================
#         # DRAW
#         # ===============================

#         cv2.rectangle(frame, (px1, py1), (px2, py2), color, 2)

#         label = f"ID {track_id} | {name} | {posture} | {status}"

#         cv2.putText(frame, label,
#                     (px1, py1 - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.5,
#                     color,
#                     2)

#     out.write(frame)

#     display_frame = cv2.resize(frame, (1000, 700))
#     cv2.imshow("Smart AI Surveillance System", display_frame)

#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# cap.release()
# out.release()
# cv2.destroyAllWindows()

import cv2
import os
import numpy as np
import mediapipe as mp
import face_recognition
from ultralytics import YOLO

# ==========================================================
# LOAD MODELS
# ==========================================================

person_model = YOLO("yolov8s.pt")
weapon_model = YOLO(r"runs\detect\weapon_model\weights\best.pt")
face_model = YOLO("yolov8n-face.pt")   # Face detection model

# ==========================================================
# MEDIAPIPE POSE
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
# HELPER STRUCTURES
# ==========================================================

armed_ids = set()
identity_map = {}

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
    "output_face.mp4",
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

    # ---------------- PERSON TRACKING ----------------
    person_results = person_model.track(
        frame,
        persist=True,
        conf=0.4,
        classes=[0],
        verbose=False
    )

    # ---------------- WEAPON DETECTION ----------------
    weapon_results = weapon_model(frame, conf=0.55, verbose=False)

    # ---------------- FACE DETECTION ----------------
    face_results = face_model(frame, conf=0.5, verbose=False)

    persons = []
    weapons = []
    faces = []

    # Collect persons
    if person_results[0].boxes.id is not None:
        for box, track_id in zip(
                person_results[0].boxes.xyxy,
                person_results[0].boxes.id):

            x1, y1, x2, y2 = map(int, box)
            track_id = int(track_id)
            persons.append((track_id, x1, y1, x2, y2))

    # Collect weapons
    for box in weapon_results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        weapons.append((x1, y1, x2, y2))

    # Collect faces
    for box in face_results[0].boxes:
        fx1, fy1, fx2, fy2 = map(int, box.xyxy[0])
        faces.append((fx1, fy1, fx2, fy2))

    # ---------------- ASSOCIATE WEAPON TO PERSON ----------------
    for wx1, wy1, wx2, wy2 in weapons:
        cx = (wx1 + wx2) // 2
        cy = (wy1 + wy2) // 2

        for track_id, px1, py1, px2, py2 in persons:
            if px1 <= cx <= px2 and py1 <= cy <= py2:
                armed_ids.add(track_id)

    # ---------------- PROCESS EACH PERSON ----------------
    for track_id, px1, py1, px2, py2 in persons:

        person_roi = frame[py1:py2, px1:px2]

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

        # ================= COLOR LOGIC =================
        if track_id in armed_ids:
            color = (0, 0, 255)
            status = "ARMED"
        else:
            color = (0, 255, 0)
            status = "NORMAL"

        # ================= DRAW =================
        cv2.rectangle(frame, (px1, py1), (px2, py2), color, 2)

        label = f"ID {track_id} | {name} | {posture} | {status}"

        (text_width, text_height), _ = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)



        for wx1, wy1, wx2, wy2 in weapons:
            cv2.rectangle(frame, (wx1, wy1), (wx2, wy2),
                      (0, 255, 255), 2)
            cv2.putText(frame, "Weapon",
                    (wx1, wy1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 255), 2)
            
        # Auto positioning (inside if near top)
        if py1 - text_height - 10 < 0:
            text_y = py1 + text_height + 10
        else:
            text_y = py1 - 10

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