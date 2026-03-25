import cv2
import os
from app.detection.yolo_person import PersonDetector
from app.detection.yolo_weapon import WeaponDetector

# ------------------ CONFIG ------------------
PERSON_MODEL = "models/yolo/yolov8s.pt"
WEAPON_MODEL = "models/yolo/weapon.pt"

VIDEO_PATH = "Sample_data/Person/Video/video.mp4"
OUTPUT_DIR = "Outputs/step3_memory_result"


PERSON_MODEL = "models/yolov8s.pt"
WEAPON_MODEL = "runs/detect/weapon_model/weights/best.pt"

VIDEO_PATH = "Sample_data/Tracking/Prediction.avi"
OUTPUT_DIR = "Outputs/tracking_result"

DEBUG = True

# 🔥 MEMORY SETTINGS
MEMORY_FRAMES = 50  # keep "armed" state for N frames

# ------------------ SETUP ------------------
os.makedirs(OUTPUT_DIR, exist_ok=True)
output_path = os.path.join(OUTPUT_DIR, "tracking_output.mp4")

person_detector = PersonDetector(PERSON_MODEL)
weapon_detector = WeaponDetector(WEAPON_MODEL)

cap = cv2.VideoCapture(VIDEO_PATH)

width = int(cap.get(3))
height = int(cap.get(4))
fps = int(cap.get(cv2.CAP_PROP_FPS))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

print("\n🚀 Step 3: Tracking + Association + Memory...\n")

# ------------------ MEMORY STORAGE ------------------
armed_memory = {}   # {person_id: remaining_frames}

# ------------------ HELPER FUNCTION ------------------
def is_inside(person_box, weapon_box):
    px1, py1, px2, py2 = person_box
    wx1, wy1, wx2, wy2 = weapon_box

    return (wx1 >= px1 and wy1 >= py1 and wx2 <= px2 and wy2 <= py2)

# ------------------ MAIN LOOP ------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 🔍 Detect
    persons = person_detector.detect(frame)
    weapons = weapon_detector.detect(frame)

    # ------------------ ASSOCIATION ------------------
    current_armed = set()

    for person in persons:
        for weapon in weapons:
            if is_inside(person["bbox"], weapon["bbox"]):
                current_armed.add(person["id"])

    # ------------------ MEMORY UPDATE ------------------
    # Add/update memory for detected armed persons
    for pid in current_armed:
        armed_memory[pid] = MEMORY_FRAMES

    # Decrease memory count
    for pid in list(armed_memory.keys()):
        armed_memory[pid] -= 1
        if armed_memory[pid] <= 0:
            del armed_memory[pid]

    # Final armed persons after memory stabilization
    armed_person_ids = set(armed_memory.keys())

    # ------------------ DRAW PERSONS ------------------
    for person in persons:
        x1, y1, x2, y2 = map(int, person["bbox"])
        pid = person["id"]

        if pid in armed_person_ids:
            color = (0, 0, 255)  # RED
            label = f"ARMED ID:{pid}"
        else:
            color = (0, 255, 0)  # GREEN
            label = f"SAFE ID:{pid}"

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # ------------------ DRAW WEAPONS ------------------
    for weapon in weapons:
        x1, y1, x2, y2 = map(int, weapon["bbox"])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, "Weapon", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # ------------------ RISK LOGIC ------------------
    if armed_person_ids:
        risk = "HIGH"
    elif weapons:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    # Display risk
    color = (0, 255, 0)
    if risk == "MEDIUM":
        color = (0, 165, 255)
    elif risk == "HIGH":
        color = (0, 0, 255)

    cv2.putText(frame, f"Risk: {risk}",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, color, 3)

    # ------------------ DEBUG PRINT ------------------
    if risk != "LOW":
        print(f"[ALERT] {risk} | Armed IDs: {armed_person_ids}")

    # ------------------ SAVE ------------------
    out.write(frame)

    # ------------------ DISPLAY ------------------
    if DEBUG:
        cv2.imshow("Step 3 - Memory Tracking", frame)

        if cv2.waitKey(1) == 27:  # ESC
            break

# ------------------ CLEANUP ------------------
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"\n✅ Output saved at: {output_path}")
print("🎯 Step 3 with memory completed successfully!")