
import cv2
import os
from app.detection.yolo_person import PersonDetector

#  CONFIG 
MODEL_PATH = "models/yolov8s.pt"

IMAGE_FOLDER = "Sample_data/Person/Images"
VIDEO_FOLDER = "Sample_data/Person/Video"
OUTPUT_FOLDER = "Outputs/person_result"

DEBUG = True  # True → show windows, False → silent

# SETUP 
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

detector = PersonDetector(MODEL_PATH)

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
        label = f"{det.get('label', 'person')} {det.get('confidence', 0):.2f}"

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Save image
    save_path = os.path.join(OUTPUT_FOLDER, f"img_{img_file}")
    cv2.imwrite(save_path, frame)

    print(f" Image processed: {img_file}")

    #  Show image
    if DEBUG:
        cv2.imshow("Image Detection", frame)
        key = cv2.waitKey(0)

        if key == 27:
            break

cv2.destroyAllWindows()

#  VIDEO TEST 
print("\n🎥 Starting Video Testing...\n")

for vid_file in os.listdir(VIDEO_FOLDER):
    vid_path = os.path.join(VIDEO_FOLDER, vid_file)

    cap = cv2.VideoCapture(vid_path)

    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    output_path = os.path.join(OUTPUT_FOLDER, f"vid_{vid_file}")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    print(f" Processing video: {vid_file}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detections = detector.detect(frame)

        for det in detections:
            x1, y1, x2, y2 = map(int, det["bbox"])
            label = f"{det.get('label', 'person')} {det.get('confidence', 0):.2f}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        out.write(frame)

        if DEBUG:
            cv2.imshow("Video Detection", frame)
            key = cv2.waitKey(1)

            if key == 27:
                break

    cap.release()
    out.release()

    print(f" Video saved: {vid_file}")

cv2.destroyAllWindows()

print("\n All processing completed successfully!")