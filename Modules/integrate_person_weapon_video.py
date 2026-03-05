import cv2
from ultralytics import YOLO

# ---------------------------
# Load Models
# ---------------------------
person_model = YOLO("yolov8s.pt")
weapon_model = YOLO(r"runs\detect\weapon_model\weights\best.pt")

video_path = "Prediction1.avi"
cap = cv2.VideoCapture(video_path)

# ---------------------------
# Video Writer (SAVE OUTPUT)
# ---------------------------
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(
    "output_surveillance.mp4",
    fourcc,
    fps,
    (frame_width, frame_height)
)

# ---------------------------
# Create Window
# ---------------------------
cv2.namedWindow("Smart Surveillance System", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Smart Surveillance System", 1280, 720)

armed_ids = set()


# ---------------------------
# Main Loop
# ---------------------------
while True:

    ret, frame = cap.read()
    if not ret:
        break

    # ---- Person Tracking ----
    person_results = person_model.track(
        frame,
        persist=True,
        conf=0.4,
        classes=[0],
        verbose=False
    )

    # ---- Weapon Detection ----
    weapon_results = weapon_model(frame, conf=0.55, verbose=False)

    persons = []
    weapons = []

    # -------- Collect Persons --------
    if person_results[0].boxes.id is not None:
        for box, track_id in zip(
                person_results[0].boxes.xyxy,
                person_results[0].boxes.id):

            px1, py1, px2, py2 = map(int, box)
            persons.append((int(track_id), px1, py1, px2, py2))

    # -------- Collect Weapons --------
    for box in weapon_results[0].boxes:
        wx1, wy1, wx2, wy2 = map(int, box.xyxy[0])
        weapons.append((wx1, wy1, wx2, wy2))

    # -------- Associate Weapon to Person --------
    for wx1, wy1, wx2, wy2 in weapons:
        cx = (wx1 + wx2) // 2
        cy = (wy1 + wy2) // 2

        for track_id, px1, py1, px2, py2 in persons:
            if px1 <= cx <= px2 and py1 <= cy <= py2:
                armed_ids.add(track_id)

    # -------- Draw Weapons --------
    for wx1, wy1, wx2, wy2 in weapons:
        cv2.rectangle(frame, (wx1, wy1), (wx2, wy2),
                      (0, 255, 255), 2)
        cv2.putText(frame, "Weapon",
                    (wx1, wy1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 255), 2)

    # -------- Draw Persons --------
    for track_id, px1, py1, px2, py2 in persons:

        if track_id in armed_ids:
            color = (0, 0, 255)
            label = f"ID {track_id} - ARMED"
        else:
            color = (0, 255, 0)
            label = f"ID {track_id}"

        cv2.rectangle(frame, (px1, py1), (px2, py2),
                      color, 2)
        cv2.putText(frame, label,
                    (px1, py1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    color, 2)

    # -------- Save Frame --------
    out.write(frame)

    # -------- Show Frame --------
    cv2.imshow("Smart Surveillance System", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break


# ---------------------------
# Cleanup
# ---------------------------
cap.release()
out.release()
cv2.destroyAllWindows()