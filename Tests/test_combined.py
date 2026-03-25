import cv2
import os
from app.detection.yolo_person import PersonDetector
from app.detection.yolo_weapon import WeaponDetector

# ------------------ CONFIG ------------------
PERSON_MODEL = "models/yolov8s.pt"
WEAPON_MODEL = "runs/detect/weapon_model/weights/best.pt"

VIDEO_PATH = "Sample_data/Weapon/Video/Gun.avi"
OUTPUT_DIR = "Outputs/combined_result"

DEBUG = True  # Show window

# ------------------ SETUP ------------------
os.makedirs(OUTPUT_DIR, exist_ok=True)

output_path = os.path.join(OUTPUT_DIR, "combined_output.mp4")

person_detector = PersonDetector(PERSON_MODEL)
weapon_detector = WeaponDetector(WEAPON_MODEL)

cap = cv2.VideoCapture(VIDEO_PATH)

# ✅ Check video
if not cap.isOpened():
    print("❌ Error: Cannot open video file")
    exit()

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:
    fps = 25

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# ✅ Create resizable window
cv2.namedWindow("Combined Detection", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Combined Detection", 960, 540)

print("\n🚀 Starting Combined Detection...\n")

# ------------------ LOOP ------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 🔍 Detection
    persons = person_detector.detect(frame)
    weapons = weapon_detector.detect(frame)

    # ------------------ DRAW PERSONS ------------------
    for det in persons:
        x1, y1, x2, y2 = map(int, det["bbox"])
        label = f"Person {det['confidence']:.2f}"

        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
        cv2.putText(frame, label, (x1,y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

    # ------------------ DRAW WEAPONS ------------------
    for det in weapons:
        x1, y1, x2, y2 = map(int, det["bbox"])
        label = f"Weapon {det['confidence']:.2f}"

        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,0,255), 2)
        cv2.putText(frame, label, (x1,y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

    # ------------------ RISK LOGIC ------------------
    risk = "LOW"

    if persons and weapons:
        risk = "HIGH"
    elif weapons:
        risk = "MEDIUM"

    # Display risk
    color = (0,255,0)
    if risk == "MEDIUM":
        color = (0,165,255)
    elif risk == "HIGH":
        color = (0,0,255)

    cv2.putText(frame, f"Risk: {risk}",
                (30,50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, color, 3)

    # ------------------ ALERT ------------------
    if risk != "LOW":
        print(f"[ALERT] {risk} risk detected")

    # ------------------ SAVE ------------------
    out.write(frame)

    # ------------------ DISPLAY (FIXED) ------------------
    if DEBUG:
        # ✅ Auto-scale without zoom issue
        h, w = frame.shape[:2]
        scale = 900 / w
        display_frame = cv2.resize(frame, (int(w*scale), int(h*scale)))

        cv2.imshow("Combined Detection", display_frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

# ------------------ CLEANUP ------------------
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"\n✅ Output saved at: {output_path}")
print("🎯 Combined detection completed successfully!")
# python -m Tests.test_combined