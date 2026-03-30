# import cv2
# import os
# from datetime import datetime

# from app.detection.yolo_person import PersonDetector
# from app.detection.yolo_weapon import WeaponDetector
# from app.pose.pose import PoseDetector, detect_posture
# from app.face.face_detector import FaceDetector
# from app.face.face_recognizer import FaceRecognizer
# from app.database.db import insert_event   # ✅ DB

# # ---------------- CONFIG ----------------
# PERSON_MODEL = "models/yolo/yolov8s.pt"
# WEAPON_MODEL = "runs/detect/weapon_model/weights/best.pt"
# FACE_MODEL = "models/yolo/yolov8n.pt"
# FACE_DB = "known_faces"

# VIDEO_PATH = "Sample_data/final_pipeline/Prediction.avi"

# # ---------------- OUTPUT ----------------
# OUTPUT_DIR = "Outputs/final result"
# os.makedirs(OUTPUT_DIR, exist_ok=True)
# OUTPUT_PATH = os.path.join(OUTPUT_DIR, "final_result.avi")

# # ---------------- INIT ----------------
# print("🚀 Initializing models...")

# person_detector = PersonDetector(PERSON_MODEL)
# weapon_detector = WeaponDetector(WEAPON_MODEL)
# pose_detector = PoseDetector()
# face_detector = FaceDetector(FACE_MODEL)

# try:
#     face_recognizer = FaceRecognizer(FACE_DB)
# except:
#     face_recognizer = None

# print("✅ All models loaded")

# # ---------------- VIDEO ----------------
# cap = cv2.VideoCapture(VIDEO_PATH)

# if not cap.isOpened():
#     print("❌ Cannot open video")
#     exit()

# fps = cap.get(cv2.CAP_PROP_FPS)
# if fps == 0:
#     fps = 25

# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# fourcc = cv2.VideoWriter_fourcc(*"XVID")
# out = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (width, height))

# print("🎥 Processing video...")

# # ---------------- HELPER ----------------
# def is_inside(person_box, obj_box):
#     px1, py1, px2, py2 = person_box
#     ox1, oy1, ox2, oy2 = obj_box
#     return (ox1 >= px1 and oy1 >= py1 and ox2 <= px2 and oy2 <= py2)

# def iou(boxA, boxB):
#     xA = max(boxA[0], boxB[0])
#     yA = max(boxA[1], boxB[1])
#     xB = min(boxA[2], boxB[2])
#     yB = min(boxA[3], boxB[3])

#     inter = max(0, xB - xA) * max(0, yB - yA)

#     areaA = (boxA[2]-boxA[0]) * (boxA[3]-boxA[1])
#     areaB = (boxB[2]-boxB[0]) * (boxB[3]-boxB[1])

#     return inter / (areaA + areaB - inter + 1e-6)

# # 🔥 Memory
# ARMED_BUFFER = 100
# armed_memory = {}

# # 🔥 DB state memory (IMPORTANT)
# last_state = {}

# # ---------------- LOOP ----------------
# while True:
#     ret, frame = cap.read()

#     if not ret:
#         print("✅ Video finished")
#         break

#     persons = person_detector.detect(frame)
#     weapons = weapon_detector.detect(frame)
#     faces = face_detector.detect(frame)

#     # ---------------- POSE ----------------
#     pose_results = pose_detector.process(frame)
#     posture = "UNKNOWN"

#     if pose_results and pose_results.pose_landmarks:
#         posture = detect_posture(
#             pose_results.pose_landmarks,
#             frame.shape[0],
#             frame.shape[1]
#         )

#     # ---------------- FACE ----------------
#     face_names = []

#     if face_recognizer:
#         for (x1, y1, x2, y2) in faces:
#             h, w = frame.shape[:2]
#             x1, y1 = max(0, int(x1)), max(0, int(y1))
#             x2, y2 = min(w, int(x2)), min(h, int(y2))

#             face_crop = frame[y1:y2, x1:x2]

#             if face_crop.size == 0:
#                 continue

#             name = face_recognizer.recognize(face_crop)

#             face_names.append({
#                 "name": name,
#                 "bbox": [x1, y1, x2, y2]
#             })

#     # ---------------- WEAPON MEMORY ----------------
#     new_memory = {}

#     for person in persons:
#         px1, py1, px2, py2 = map(int, person["bbox"])
#         current_box = [px1, py1, px2, py2]

#         matched_key = None

#         for old_box in armed_memory:
#             if iou(current_box, list(old_box)) > 0.5:
#                 matched_key = old_box
#                 break

#         detected_weapon = any(
#             is_inside(current_box, list(map(int, w["bbox"])))
#             for w in weapons
#         )

#         if detected_weapon:
#             new_memory[tuple(current_box)] = ARMED_BUFFER
#         elif matched_key:
#             new_memory[tuple(current_box)] = max(0, armed_memory[matched_key] - 1)
#         else:
#             new_memory[tuple(current_box)] = 0

#     armed_memory = new_memory

#     # ---------------- FLAGS ----------------
#     armed_flags = []
#     person_names = ["Unknown"] * len(persons)

#     for person in persons:
#         box = tuple(map(int, person["bbox"]))
#         armed_flags.append(armed_memory.get(box, 0) > 0)

#     # ---------------- FACE → PERSON ----------------
#     for i, person in enumerate(persons):
#         px1, py1, px2, py2 = map(int, person["bbox"])

#         for face in face_names:
#             fx1, fy1, fx2, fy2 = face["bbox"]

#             if fx1 >= px1 and fy1 >= py1 and fx2 <= px2 and fy2 <= py2:
#                 person_names[i] = face["name"]

#     # ---------------- DRAW ----------------
#     h, w = frame.shape[:2]

#     if len(persons) == 0:
#         cv2.putText(frame, "No Person Detected",
#                     (30, 100),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     1, (0, 255, 255), 2)

#     for i, person in enumerate(persons):
#         x1, y1, x2, y2 = map(int, person["bbox"])

#         name = person_names[i]
#         status = "ARMED" if armed_flags[i] else "SAFE"

#         color = (0, 0, 255) if armed_flags[i] else (0, 255, 0)
#         label = f"{name} | {status} | {posture}"

#         text_x = max(0, min(x1, w - 200))
#         text_y = max(20, y1 - 10)

#         cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
#         cv2.putText(frame, label,
#                     (text_x, text_y),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.5, color, 2)

#     # ---------------- RISK ----------------
#     if any(armed_flags):
#         risk = "HIGH"
#     elif weapons:
#         risk = "MEDIUM"
#     elif posture == "FALLEN":
#         risk = "MEDICAL"
#     else:
#         risk = "LOW"

#     cv2.putText(frame, f"RISK: {risk}",
#                 (30, 50),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 1, (0, 0, 255), 3)

#     # ---------------- 🔥 SMART DB LOGGING ----------------
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     for i, person in enumerate(persons):
#         name = person_names[i]
#         status = "ARMED" if armed_flags[i] else "SAFE"

#         key = name if name != "Unknown" else f"person_{i}"
#         current_state = (status, posture, risk)

#         if key not in last_state or last_state[key] != current_state:

#             if risk != "LOW":
#                 insert_event(timestamp, name, status, posture, risk)
#                 print(f"📝 Logged: {name} | {status} | {posture} | {risk}")

#             last_state[key] = current_state

#     # ---------------- SAVE ----------------
#     frame = cv2.resize(frame, (width, height))
#     out.write(frame)

#     # ---------------- DISPLAY ----------------
#     cv2.imshow("SMART AI SURVEILLANCE", frame)

#     if cv2.waitKey(1) == 27:
#         break

# # ---------------- CLEANUP ----------------
# cap.release()
# out.release()
# cv2.destroyAllWindows()

# print("✅ Output saved:", OUTPUT_PATH)



import cv2
import os
from datetime import datetime

from app.detection.yolo_person import PersonDetector
from app.detection.yolo_weapon import WeaponDetector
from app.pose.pose import PoseDetector, detect_posture
from app.face.face_detector import FaceDetector
from app.face.face_recognizer import FaceRecognizer
from app.database.db import insert_event   # ✅ DB

# ---------------- CONFIG ----------------
PERSON_MODEL = "models/yolo/yolov8s.pt"
WEAPON_MODEL = "runs/detect/weapon_model/weights/best.pt"
FACE_MODEL = "models/yolo/yolov8n.pt"
FACE_DB = "known_faces"

VIDEO_PATH = "Sample_data/final_pipeline/Prediction.avi"

# ---------------- OUTPUT ----------------
OUTPUT_DIR = "Outputs/db_result"
os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT_PATH = os.path.join(OUTPUT_DIR, "db_video_result.avi")
LOG_FILE = os.path.join(OUTPUT_DIR, "db_logs.txt")   # ✅ NEW

# ---------------- INIT ----------------
print("🚀 Initializing models...")

person_detector = PersonDetector(PERSON_MODEL)
weapon_detector = WeaponDetector(WEAPON_MODEL)
pose_detector = PoseDetector()
face_detector = FaceDetector(FACE_MODEL)

try:
    face_recognizer = FaceRecognizer(FACE_DB)
except:
    face_recognizer = None

print("✅ All models loaded")

# ---------------- VIDEO ----------------
cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("❌ Cannot open video")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:
    fps = 25

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (width, height))

print("🎥 Processing video...")

# ---------------- HELPER ----------------
def is_inside(person_box, obj_box):
    px1, py1, px2, py2 = person_box
    ox1, oy1, ox2, oy2 = obj_box
    return (ox1 >= px1 and oy1 >= py1 and ox2 <= px2 and oy2 <= py2)

def iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    inter = max(0, xB - xA) * max(0, yB - yA)

    areaA = (boxA[2]-boxA[0]) * (boxA[3]-boxA[1])
    areaB = (boxB[2]-boxB[0]) * (boxB[3]-boxB[1])

    return inter / (areaA + areaB - inter + 1e-6)

# 🔥 Memory
ARMED_BUFFER = 100
armed_memory = {}

# 🔥 DB state memory
last_state = {}

# ---------------- LOOP ----------------
while True:
    ret, frame = cap.read()

    if not ret:
        print("✅ Video finished")
        break

    persons = person_detector.detect(frame)
    weapons = weapon_detector.detect(frame)
    faces = face_detector.detect(frame)

    # ---------------- POSE ----------------
    pose_results = pose_detector.process(frame)
    posture = "UNKNOWN"

    if pose_results and pose_results.pose_landmarks:
        posture = detect_posture(
            pose_results.pose_landmarks,
            frame.shape[0],
            frame.shape[1]
        )

    # ---------------- FACE ----------------
    face_names = []

    if face_recognizer:
        for (x1, y1, x2, y2) in faces:
            h, w = frame.shape[:2]
            x1, y1 = max(0, int(x1)), max(0, int(y1))
            x2, y2 = min(w, int(x2)), min(h, int(y2))

            face_crop = frame[y1:y2, x1:x2]

            if face_crop.size == 0:
                continue

            name = face_recognizer.recognize(face_crop)

            face_names.append({
                "name": name,
                "bbox": [x1, y1, x2, y2]
            })

    # ---------------- WEAPON MEMORY ----------------
    new_memory = {}

    for person in persons:
        px1, py1, px2, py2 = map(int, person["bbox"])
        current_box = [px1, py1, px2, py2]

        matched_key = None

        for old_box in armed_memory:
            if iou(current_box, list(old_box)) > 0.5:
                matched_key = old_box
                break

        detected_weapon = any(
            is_inside(current_box, list(map(int, w["bbox"])))
            for w in weapons
        )

        if detected_weapon:
            new_memory[tuple(current_box)] = ARMED_BUFFER
        elif matched_key:
            new_memory[tuple(current_box)] = max(0, armed_memory[matched_key] - 1)
        else:
            new_memory[tuple(current_box)] = 0

    armed_memory = new_memory

    # ---------------- FLAGS ----------------
    armed_flags = []
    person_names = ["Unknown"] * len(persons)

    for person in persons:
        box = tuple(map(int, person["bbox"]))
        armed_flags.append(armed_memory.get(box, 0) > 0)

    # ---------------- FACE → PERSON ----------------
    for i, person in enumerate(persons):
        px1, py1, px2, py2 = map(int, person["bbox"])

        for face in face_names:
            fx1, fy1, fx2, fy2 = face["bbox"]

            if fx1 >= px1 and fy1 >= py1 and fx2 <= px2 and fy2 <= py2:
                person_names[i] = face["name"]

    # ---------------- DRAW ----------------
    h, w = frame.shape[:2]

    if len(persons) == 0:
        cv2.putText(frame, "No Person Detected",
                    (30, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 255), 2)

    for i, person in enumerate(persons):
        x1, y1, x2, y2 = map(int, person["bbox"])

        name = person_names[i]
        status = "ARMED" if armed_flags[i] else "SAFE"

        color = (0, 0, 255) if armed_flags[i] else (0, 255, 0)
        label = f"{name} | {status} | {posture}"

        text_x = max(0, min(x1, w - 200))
        text_y = max(20, y1 - 10)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, label,
                    (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, color, 2)

    # ---------------- RISK ----------------
    if any(armed_flags):
        risk = "HIGH"
    elif weapons:
        risk = "MEDIUM"
    elif posture == "FALLEN":
        risk = "MEDICAL"
    else:
        risk = "LOW"

    cv2.putText(frame, f"RISK: {risk}",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 3)

    # ---------------- DB LOGGING ----------------
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for i, person in enumerate(persons):
        name = person_names[i]
        status = "ARMED" if armed_flags[i] else "SAFE"

        key = name if name != "Unknown" else f"person_{i}"
        current_state = (status, posture, risk)

        if key not in last_state or last_state[key] != current_state:

            if risk != "LOW":
                insert_event(timestamp, name, status, posture, risk)

                # ✅ Save to file
                log_text = f"{timestamp} | {name} | {status} | {posture} | {risk}\n"
                with open(LOG_FILE, "a") as f:
                    f.write(log_text)

                print(f"📝 Logged: {name} | {status} | {posture} | {risk}")

            last_state[key] = current_state

    # ---------------- SAVE ----------------
    frame = cv2.resize(frame, (width, height))
    out.write(frame)

    # ---------------- DISPLAY ----------------
    cv2.imshow("SMART AI SURVEILLANCE", frame)

    if cv2.waitKey(1) == 27:
        break

# ---------------- CLEANUP ----------------
cap.release()
out.release()
cv2.destroyAllWindows()

print("✅ Output saved:", OUTPUT_PATH)
print("📄 Logs saved:", LOG_FILE)