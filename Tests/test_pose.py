import cv2
import os

from app.detection.yolo_person import PersonDetector
from app.pose.pose import PoseDetector, detect_posture

# ---------------- CONFIG ----------------
PERSON_MODEL = "models/yolov8s.pt"

IMAGE_FOLDER = "Sample_data/Pose/Images"
VIDEO_FOLDER = "Sample_data/Pose/Video"

OUTPUT_FOLDER = "Outputs/pose_result"

# ---------------- INIT ----------------
person_detector = PersonDetector(PERSON_MODEL)
pose_detector = PoseDetector()

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

print("\n🚀 Running Pose Detection (MULTI FILE SUPPORT)\n")


# ---------- DRAW LABEL ----------
def draw_label(frame, text, x1, y1, color):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    thickness = 2

    (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)

    if y1 - 10 > text_h:
        text_x = x1
        text_y = y1 - 10
    else:
        text_x = x1 + 5
        text_y = y1 + text_h + 5

    cv2.rectangle(frame,
                  (text_x - 2, text_y - text_h - 2),
                  (text_x + text_w + 2, text_y + 2),
                  color, -1)

    cv2.putText(frame, text, (text_x, text_y),
                font, font_scale, (255, 255, 255), thickness)


# ================= IMAGE =================
image_files = [f for f in os.listdir(IMAGE_FOLDER)
               if f.lower().endswith((".jpg", ".jpeg", ".png"))]

print(f"📸 Total Images Found: {len(image_files)}")

for file in image_files:

    path = os.path.join(IMAGE_FOLDER, file)
    frame = cv2.imread(path)

    if frame is None:
        continue

    print(f"🖼️ Processing Image: {file}")

    persons = person_detector.detect(frame)

    for p in persons:
        x1, y1, x2, y2 = map(int, p["bbox"])

        pad = 20
        x1 = max(0, x1 - pad)
        y1 = max(0, y1 - pad)
        x2 = min(frame.shape[1], x2 + pad)
        y2 = min(frame.shape[0], y2 + pad)

        person_crop = frame[y1:y2, x1:x2]

        posture = "STANDING"

        if person_crop.size != 0:
            results = pose_detector.process(person_crop)

            if results and results.pose_landmarks:
                posture = detect_posture(
                    results.pose_landmarks,
                    person_crop.shape[0],
                    person_crop.shape[1]
                )

        color = (0, 255, 0) if posture == "STANDING" else (0, 0, 255)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        draw_label(frame, posture, x1, y1, color)

    # SAVE IMAGE
    output_path = os.path.join(OUTPUT_FOLDER, f"output_{file}")
    cv2.imwrite(output_path, frame)

    # SHOW IMAGE
    cv2.imshow("Image Pose", frame)

    key = cv2.waitKey(0)

    # ESC → skip this image, continue next
    if key == 27:
        continue

cv2.destroyAllWindows()


# ================= VIDEO =================
video_files = [f for f in os.listdir(VIDEO_FOLDER)
               if f.lower().endswith((".mp4", ".avi", ".mov"))]

print(f"\n🎥 Total Videos Found: {len(video_files)}")

for file in video_files:

    path = os.path.join(VIDEO_FOLDER, file)
    cap = cv2.VideoCapture(path)

    if not cap.isOpened():
        print(f"❌ Cannot open {file}")
        continue

    print(f"▶️ Processing Video: {file}")

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output_path = os.path.join(OUTPUT_FOLDER, f"output_{file}")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        persons = person_detector.detect(frame)

        for p in persons:
            x1, y1, x2, y2 = map(int, p["bbox"])

            pad = 20
            x1 = max(0, x1 - pad)
            y1 = max(0, y1 - pad)
            x2 = min(frame.shape[1], x2 + pad)
            y2 = min(frame.shape[0], y2 + pad)

            person_crop = frame[y1:y2, x1:x2]

            posture = "STANDING"

            if person_crop.size != 0:
                results = pose_detector.process(person_crop)

                if results and results.pose_landmarks:
                    posture = detect_posture(
                        results.pose_landmarks,
                        person_crop.shape[0],
                        person_crop.shape[1]
                    )

            color = (0, 255, 0) if posture == "STANDING" else (0, 0, 255)

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            draw_label(frame, posture, x1, y1, color)

        out.write(frame)
        cv2.imshow("Video Pose", frame)

        key = cv2.waitKey(1)

        # ESC → skip current video only
        if key == 27:
            break

    cap.release()
    out.release()

cv2.destroyAllWindows()

print("\n✅ ALL FILES PROCESSED & SAVED\n")