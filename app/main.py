# # # import cv2
# # # import os
# # # import sys

# # # sys.excepthook = sys.__excepthook__

# # # from app.detection.yolo_person import PersonDetector
# # # from app.detection.yolo_weapon import WeaponDetector
# # # from app.pose.pose import PoseDetector, detect_posture
# # # from app.face.face_detector import FaceDetector
# # # from app.face.face_recognizer import FaceRecognizer

# # # # ---------------- CONFIG ----------------
# # # PERSON_MODEL = "models/yolo/yolov8s.pt"
# # # WEAPON_MODEL = "runs/detect/weapon_model/weights/best.pt"
# # # FACE_MODEL = "models/yolo/yolov8n.pt"
# # # FACE_DB = "known_faces"

# # # VIDEO_PATH = "Sample_data/final_pipeline/Prediction.avi"

# # # # ---------------- OUTPUT ----------------
# # # OUTPUT_DIR = "Outputs/final result"
# # # os.makedirs(OUTPUT_DIR, exist_ok=True)
# # # OUTPUT_PATH = os.path.join(OUTPUT_DIR, "final_result.avi")

# # # # ---------------- INIT ----------------
# # # try:
# # #     print("Loading PersonDetector...")
# # #     person_detector = PersonDetector(PERSON_MODEL)

# # #     print("Loading WeaponDetector...")
# # #     weapon_detector = WeaponDetector(WEAPON_MODEL)

# # #     print("Loading PoseDetector...")
# # #     pose_detector = PoseDetector()

# # #     print("Loading FaceDetector...")
# # #     face_detector = FaceDetector(FACE_MODEL)

# # #     print("Loading FaceRecognizer...")
# # #     face_recognizer = FaceRecognizer(FACE_DB)

# # #     print("✅ ALL MODELS LOADED")

# # # except Exception as e:
# # #     print("🔥 INIT ERROR:", e)
# # #     exit()

# # # # ---------------- VIDEO ----------------
# # # cap = cv2.VideoCapture(VIDEO_PATH)

# # # if not cap.isOpened():
# # #     print("❌ ERROR: Cannot open video")
# # #     exit()

# # # fps = cap.get(cv2.CAP_PROP_FPS)
# # # if fps == 0:
# # #     fps = 25

# # # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# # # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# # # print(f"🎥 FPS: {fps}, Width: {width}, Height: {height}")

# # # fourcc = cv2.VideoWriter_fourcc(*"XVID")
# # # out = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (width, height))

# # # # ---------------- HELPER ----------------
# # # def is_inside(person_box, obj_box):
# # #     px1, py1, px2, py2 = person_box
# # #     ox1, oy1, ox2, oy2 = obj_box
# # #     return (ox1 >= px1 and oy1 >= py1 and ox2 <= px2 and oy2 <= py2)

# # # # ---------------- LOOP ----------------
# # # frame_count = 0

# # # while True:
# # #     ret, frame = cap.read()

# # #     if not ret:
# # #         print("⚠️ No more frames OR video read failed")
# # #         break

# # #     frame_count += 1
# # #     print(f"➡️ Processing frame {frame_count}")

# # #     # 🔥 CRITICAL FIX: ensure frame valid
# # #     if frame is None or frame.size == 0:
# # #         print("❌ Empty frame")
# # #         continue

# # #     try:
# # #         persons = person_detector.detect(frame)
# # #         weapons = weapon_detector.detect(frame)
# # #         faces = face_detector.detect(frame)
# # #         pose_results = pose_detector.process(frame)
# # #     except Exception as e:
# # #         print("🔥 CRASH:", e)
# # #         break

# # #     # ---------------- POSE ----------------
# # #     posture = "UNKNOWN"
# # #     if pose_results and pose_results.pose_landmarks:
# # #         posture = detect_posture(
# # #             pose_results.pose_landmarks,
# # #             frame.shape[0],
# # #             frame.shape[1]
# # #         )

# # #     # ---------------- DRAW ----------------
# # #     for person in persons:
# # #         x1, y1, x2, y2 = map(int, person["bbox"])
# # #         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

# # #     # ---------------- SAVE ----------------
# # #     frame = cv2.resize(frame, (width, height))

# # #     out.write(frame)

# # #     # ---------------- DISPLAY ----------------
# # #     cv2.imshow("SMART AI SURVEILLANCE", frame)

# # #     if cv2.waitKey(1) == 27:
# # #         break

# # # print(f"✅ Total frames processed: {frame_count}")

# # # # ---------------- CLEANUP ----------------
# # # cap.release()
# # # out.release()
# # # cv2.destroyAllWindows()

# # # print("✅ Video saved at:", OUTPUT_PATH)



# # import cv2
# # import os

# # from app.detection.yolo_person import PersonDetector
# # from app.detection.yolo_weapon import WeaponDetector
# # from app.pose.pose import PoseDetector, detect_posture
# # from app.face.face_detector import FaceDetector
# # from app.face.face_recognizer import FaceRecognizer

# # # ---------------- CONFIG ----------------
# # PERSON_MODEL = "models/yolo/yolov8s.pt"
# # WEAPON_MODEL = "runs/detect/weapon_model/weights/best.pt"
# # FACE_MODEL = "models/yolo/yolov8n.pt"
# # FACE_DB = "known_faces"

# # VIDEO_PATH = "Sample_data/final_pipeline/Prediction.avi"

# # # ---------------- OUTPUT ----------------
# # OUTPUT_DIR = "Outputs/final result"
# # os.makedirs(OUTPUT_DIR, exist_ok=True)
# # OUTPUT_PATH = os.path.join(OUTPUT_DIR, "final_result.avi")

# # # ---------------- INIT ----------------
# # print("🚀 Initializing models...")

# # person_detector = PersonDetector(PERSON_MODEL)
# # weapon_detector = WeaponDetector(WEAPON_MODEL)
# # pose_detector = PoseDetector()
# # face_detector = FaceDetector(FACE_MODEL)

# # # ✅ FIX: safe face recognizer
# # try:
# #     face_recognizer = FaceRecognizer(FACE_DB)
# # except Exception as e:
# #     print("⚠️ FaceRecognizer error:", e)
# #     face_recognizer = None

# # print("✅ All models loaded")

# # # ---------------- VIDEO ----------------
# # cap = cv2.VideoCapture(VIDEO_PATH)

# # if not cap.isOpened():
# #     print("❌ Cannot open video")
# #     exit()

# # fps = cap.get(cv2.CAP_PROP_FPS)
# # if fps == 0:
# #     fps = 25

# # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# # fourcc = cv2.VideoWriter_fourcc(*"XVID")
# # out = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (width, height))

# # print("🎥 Processing video...")

# # # ---------------- HELPER ----------------
# # def is_inside(person_box, obj_box):
# #     px1, py1, px2, py2 = person_box
# #     ox1, oy1, ox2, oy2 = obj_box
# #     return (ox1 >= px1 and oy1 >= py1 and ox2 <= px2 and oy2 <= py2)

# # # ---------------- LOOP ----------------
# # while True:
# #     ret, frame = cap.read()

# #     if not ret:
# #         print("✅ Video finished")
# #         break

# #     persons = person_detector.detect(frame)
# #     weapons = weapon_detector.detect(frame)
# #     faces = face_detector.detect(frame)

# #     pose_results = pose_detector.process(frame)
# #     posture = "UNKNOWN"

# #     if pose_results and pose_results.pose_landmarks:
# #         posture = detect_posture(
# #             pose_results.pose_landmarks,
# #             frame.shape[0],
# #             frame.shape[1]
# #         )

# #     # ---------------- FACE ----------------
# #     face_names = []

# #     if face_recognizer:
# #         for (x1, y1, x2, y2) in faces:
# #             h, w = frame.shape[:2]

# #             x1, y1 = max(0, int(x1)), max(0, int(y1))
# #             x2, y2 = min(w, int(x2)), min(h, int(y2))

# #             face_crop = frame[y1:y2, x1:x2]

# #             if face_crop.size == 0:
# #                 continue

# #             name = face_recognizer.recognize(face_crop)

# #             face_names.append({
# #                 "name": name,
# #                 "bbox": [x1, y1, x2, y2]
# #             })

# #     # ---------------- ASSOCIATION ----------------
# #     armed_flags = [False] * len(persons)
# #     person_names = ["Unknown"] * len(persons)

# #     for i, person in enumerate(persons):
# #         px1, py1, px2, py2 = map(int, person["bbox"])

# #         for weapon in weapons:
# #             wx1, wy1, wx2, wy2 = map(int, weapon["bbox"])

# #             if is_inside([px1, py1, px2, py2], [wx1, wy1, wx2, wy2]):
# #                 armed_flags[i] = True

# #     for i, person in enumerate(persons):
# #         px1, py1, px2, py2 = map(int, person["bbox"])

# #         for face in face_names:
# #             fx1, fy1, fx2, fy2 = face["bbox"]

# #             if fx1 >= px1 and fy1 >= py1 and fx2 <= px2 and fy2 <= py2:
# #                 person_names[i] = face["name"]

# #     # ---------------- DRAW ----------------
# #     if len(persons) == 0:
# #         cv2.putText(frame, "No Person Detected",
# #                     (30, 100),
# #                     cv2.FONT_HERSHEY_SIMPLEX,
# #                     1, (0, 255, 255), 2)

# #     for i, person in enumerate(persons):
# #         x1, y1, x2, y2 = map(int, person["bbox"])

# #         name = person_names[i]
# #         status = "ARMED" if armed_flags[i] else "SAFE"

# #         color = (0, 0, 255) if armed_flags[i] else (0, 255, 0)

# #         label = f"{name} | {status} | {posture}"

# #         cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
# #         cv2.putText(frame, label,
# #                     (x1, y1 - 10),
# #                     cv2.FONT_HERSHEY_SIMPLEX,
# #                     0.5, color, 2)

# #     # ---------------- RISK ----------------
# #     if any(armed_flags):
# #         risk = "HIGH"
# #     elif weapons:
# #         risk = "MEDIUM"
# #     elif posture == "FALLEN":
# #         risk = "MEDICAL"
# #     else:
# #         risk = "LOW"

# #     cv2.putText(frame, f"RISK: {risk}",
# #                 (30, 50),
# #                 cv2.FONT_HERSHEY_SIMPLEX,
# #                 1, (0, 0, 255), 3)

# #     # ---------------- SAVE ----------------
# #     frame = cv2.resize(frame, (width, height))
# #     out.write(frame)

# #     # ---------------- DISPLAY ----------------
# #     cv2.imshow("SMART AI SURVEILLANCE", frame)

# #     if cv2.waitKey(1) == 27:
# #         break

# # # ---------------- CLEANUP ----------------
# # cap.release()
# # out.release()
# # cv2.destroyAllWindows()

# # print("✅ Output saved:", OUTPUT_PATH)





# import cv2
# import os

# from app.detection.yolo_person import PersonDetector
# from app.detection.yolo_weapon import WeaponDetector
# from app.pose.pose import PoseDetector, detect_posture
# from app.face.face_detector import FaceDetector
# from app.face.face_recognizer import FaceRecognizer

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

# # 🔥 Weapon memory buffer
# ARMED_BUFFER = 30
# armed_memory = []

# # ---------------- LOOP ----------------
# while True:
#     ret, frame = cap.read()

#     if not ret:
#         print("✅ Video finished")
#         break

#     persons = person_detector.detect(frame)
#     weapons = weapon_detector.detect(frame)
#     faces = face_detector.detect(frame)

#     # Ensure memory size
#     if len(armed_memory) != len(persons):
#         armed_memory = [0] * len(persons)

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

#     # ---------------- ASSOCIATION ----------------
#     armed_flags = [False] * len(persons)
#     person_names = ["Unknown"] * len(persons)

#     # 🔥 WEAPON MEMORY LOGIC
#     for i, person in enumerate(persons):
#         px1, py1, px2, py2 = map(int, person["bbox"])

#         detected_weapon = False

#         for weapon in weapons:
#             wx1, wy1, wx2, wy2 = map(int, weapon["bbox"])

#             if is_inside([px1, py1, px2, py2], [wx1, wy1, wx2, wy2]):
#                 detected_weapon = True
#                 break

#         if detected_weapon:
#             armed_memory[i] = ARMED_BUFFER
#         else:
#             armed_memory[i] = max(0, armed_memory[i] - 1)

#         armed_flags[i] = armed_memory[i] > 0

#     # Face → person
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

#         # 🔥 FIX: keep label inside frame
#         text_x = max(0, min(x1, w - 200))
#         text_y = max(20, y1 - 10)

#         cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
#         cv2.putText(frame, label,
#                     (text_x, text_y),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.5, color, 2)

#     # Draw weapons
#     for weapon in weapons:
#         x1, y1, x2, y2 = map(int, weapon["bbox"])
#         cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

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

from app.detection.yolo_person import PersonDetector
from app.detection.yolo_weapon import WeaponDetector
from app.pose.pose import PoseDetector, detect_posture
from app.face.face_detector import FaceDetector
from app.face.face_recognizer import FaceRecognizer

# ---------------- CONFIG ----------------
PERSON_MODEL = "models/yolo/yolov8s.pt"
WEAPON_MODEL = "runs/detect/weapon_model/weights/best.pt"
FACE_MODEL = "models/yolo/yolov8n.pt"
FACE_DB = "known_faces"

VIDEO_PATH = "Sample_data/final_pipeline/Prediction.avi"

# ---------------- OUTPUT ----------------
OUTPUT_DIR = "Outputs/final result"
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "final_result.avi")

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

# 🔥 IoU function
def iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    inter = max(0, xB - xA) * max(0, yB - yA)

    areaA = (boxA[2]-boxA[0]) * (boxA[3]-boxA[1])
    areaB = (boxB[2]-boxB[0]) * (boxB[3]-boxB[1])

    return inter / (areaA + areaB - inter + 1e-6)

# 🔥 Weapon memory (IoU-based)
ARMED_BUFFER = 100
armed_memory = {}

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

    # ---------------- WEAPON MEMORY (IoU MATCHING) ----------------
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

        # 🔥 Keep text inside frame
        text_x = max(0, min(x1, w - 200))
        text_y = max(20, y1 - 10)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, label,
                    (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, color, 2)

    # Draw weapons
    for weapon in weapons:
        x1, y1, x2, y2 = map(int, weapon["bbox"])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

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