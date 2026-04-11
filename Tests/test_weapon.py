import cv2
import os
from app.detection.yolo_weapon import WeaponDetector

# CONFIG 
MODEL_PATH = "runs/detect/weapon_model/weights/best.pt"

IMAGE_FOLDER = "Sample_data/Weapon/Images"
VIDEO_FOLDER = "Sample_data/Weapon/Video"
OUTPUT_FOLDER = "Outputs/weapon_result"

DEBUG = True
SKIP_FRAMES = 2

# Max display size (screen fit)
MAX_WIDTH = 1200
MAX_HEIGHT = 800

#  SETUP 
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

detector = WeaponDetector(MODEL_PATH)

# HELPER FUNCTION 
def fit_to_screen(frame, max_w, max_h):
    h, w = frame.shape[:2]

    #  ONLY shrink, NEVER enlarge
    if w <= max_w and h <= max_h:
        return frame

    scale = min(max_w / w, max_h / h)

    new_w = int(w * scale)
    new_h = int(h * scale)

    return cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)

#  IMAGE TEST
print("\n Starting Image Testing...\n")

for img_file in os.listdir(IMAGE_FOLDER):
    img_path = os.path.join(IMAGE_FOLDER, img_file)

    frame = cv2.imread(img_path)
    if frame is None:
        continue

    detections = detector.detect(frame)

    for det in detections:
        x1, y1, x2, y2 = map(int, det["bbox"])
        label = f"{det['label']} {det['confidence']:.2f}"

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    save_path = os.path.join(OUTPUT_FOLDER, f"img_{img_file}")
    cv2.imwrite(save_path, frame)

    print(f" Image processed: {img_file}")

    if DEBUG:
        display_frame = fit_to_screen(frame, MAX_WIDTH, MAX_HEIGHT)

        cv2.imshow("Image Detection", display_frame)
        key = cv2.waitKey(0)

        if key == 27:
            break

cv2.destroyAllWindows()

# VIDEO TEST 
print("\n Starting Video Testing...\n")

for vid_file in os.listdir(VIDEO_FOLDER):
    vid_path = os.path.join(VIDEO_FOLDER, vid_file)

    cap = cv2.VideoCapture(vid_path)

    if not cap.isOpened():
        print(" Error opening video")
        continue

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 25

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output_path = os.path.join(OUTPUT_FOLDER, f"vid_{vid_file}")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    print(f" Processing video: {vid_file}")

    # IMPORTANT: auto-size window (no forced scaling)
    cv2.namedWindow("Video Detection", cv2.WINDOW_AUTOSIZE)

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        if frame_count % SKIP_FRAMES != 0:
            continue

        detections = detector.detect(frame)

        for det in detections:
            x1, y1, x2, y2 = map(int, det["bbox"])
            label = f"{det['label']} {det['confidence']:.2f}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        out.write(frame)

        if DEBUG:
            # FIX: only shrink if too big (no zoom)
            display_frame = fit_to_screen(frame, MAX_WIDTH, MAX_HEIGHT)

            cv2.imshow("Video Detection", display_frame)

            key = cv2.waitKey(1)

            if key == 27 or key == ord('q'):
                break
            elif key == ord('p'):
                cv2.waitKey(0)

    cap.release()
    out.release()

    print(f" Video saved: {vid_file}")

cv2.destroyAllWindows()

print("\nAll processing completed successfully!")

#  python -m Tests.test_weapon