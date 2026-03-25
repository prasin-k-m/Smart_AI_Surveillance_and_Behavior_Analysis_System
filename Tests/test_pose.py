import cv2
import os
import mediapipe as mp
from app.detection.yolo_person import PersonDetector
from app.pose.pose import PoseDetector, detect_posture

# ------------------ CONFIG ------------------
PERSON_MODEL = "models/yolov8s.pt"

IMAGE_FOLDER = "Sample_data/Pose/Images"
VIDEO_FOLDER = "Sample_data/Pose/Video"
OUTPUT_FOLDER = "Outputs/pose_result"

DEBUG = True

IMAGE_EXT = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
VIDEO_EXT = (".mp4", ".avi", ".mov", ".mkv")

# ------------------ SETUP ------------------
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

person_detector = PersonDetector(PERSON_MODEL)
mp_draw = mp.solutions.drawing_utils

print("\n🚀 Pose Detection Started...\n")

# ================== IMAGE ==================
image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(IMAGE_EXT)]
print(f"🖼️ Total Images Found: {len(image_files)}\n")

for idx, img_file in enumerate(image_files):

    try:
        img_path = os.path.join(IMAGE_FOLDER, img_file)
        print(f"➡️ Processing Image [{idx+1}/{len(image_files)}]: {img_file}")

        frame = cv2.imread(img_path)

        if frame is None:
            print(f"⚠️ Cannot read image: {img_file}")
            continue

        persons = person_detector.detect(frame)

        for person in persons:
            x1, y1, x2, y2 = map(int, person["bbox"])

            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(frame.shape[1], x2), min(frame.shape[0], y2)

            crop = frame[y1:y2, x1:x2]
            if crop.size == 0:
                continue

            crop = cv2.resize(crop, (256, 256))

            # 🔥 NEW PoseDetector per person
            pose_detector = PoseDetector()
            results = pose_detector.process(crop)

            posture = "UNKNOWN"

            if results and results.pose_landmarks:
                posture = detect_posture(
                    results.pose_landmarks,
                    crop.shape[0],
                    crop.shape[1]
                )

                mp_draw.draw_landmarks(
                    crop,
                    results.pose_landmarks,
                    pose_detector.mp_pose.POSE_CONNECTIONS
                )

            crop_back = cv2.resize(crop, (x2 - x1, y2 - y1))
            frame[y1:y2, x1:x2] = crop_back

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, posture, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        cv2.imwrite(os.path.join(OUTPUT_FOLDER, f"img_{img_file}"), frame)

        if DEBUG:
            cv2.imshow("Pose Image", frame)
            if cv2.waitKey(500) == 27:
                break

    except Exception as e:
        print(f"❌ Error processing {img_file}: {e}")

cv2.destroyAllWindows()

# ================== VIDEO ==================
video_files = [f for f in os.listdir(VIDEO_FOLDER) if f.lower().endswith(VIDEO_EXT)]
print(f"\n🎥 Total Videos Found: {len(video_files)}\n")

for vid_file in video_files:

    try:
        vid_path = os.path.join(VIDEO_FOLDER, vid_file)
        print(f"➡️ Opening Video: {vid_file}")

        cap = cv2.VideoCapture(vid_path)

        if not cap.isOpened():
            print(f"❌ Failed to open video: {vid_file}")
            continue

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 25

        out = cv2.VideoWriter(
            os.path.join(OUTPUT_FOLDER, f"vid_{vid_file}"),
            cv2.VideoWriter_fourcc(*'mp4v'),
            fps,
            (width, height)
        )

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            persons = person_detector.detect(frame)

            for person in persons:
                x1, y1, x2, y2 = map(int, person["bbox"])

                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(frame.shape[1], x2), min(frame.shape[0], y2)

                crop = frame[y1:y2, x1:x2]
                if crop.size == 0:
                    continue

                crop = cv2.resize(crop, (256, 256))

                pose_detector = PoseDetector()
                results = pose_detector.process(crop)

                posture = "UNKNOWN"

                if results and results.pose_landmarks:
                    posture = detect_posture(
                        results.pose_landmarks,
                        crop.shape[0],
                        crop.shape[1]
                    )

                    mp_draw.draw_landmarks(
                        crop,
                        results.pose_landmarks,
                        pose_detector.mp_pose.POSE_CONNECTIONS
                    )

                crop_back = cv2.resize(crop, (x2 - x1, y2 - y1))
                frame[y1:y2, x1:x2] = crop_back

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, posture, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            out.write(frame)

            if DEBUG:
                cv2.imshow("Pose Video", frame)
                if cv2.waitKey(1) == 27:
                    break

        cap.release()
        out.release()
        print(f"💾 Saved: vid_{vid_file}")

    except Exception as e:
        print(f"❌ Error processing video {vid_file}: {e}")

cv2.destroyAllWindows()

print("\n🎯 All processing completed successfully!")