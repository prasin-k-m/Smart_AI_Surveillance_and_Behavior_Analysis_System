
import cv2
import os
from app.face.face_recognizer import FaceRecognizer
from app.face.face_detector import FaceDetector

# USE YOLO FACE MODEL HERE
face_detector = FaceDetector("models/yolov8n-face.pt")
face_recognizer = FaceRecognizer("Sample_data/Known_faces/Images", tolerance=0.6)

video_path = r"Sample_data/Known_faces/video/face.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(" Cannot open video")
    exit()

output_dir = "Outputs/face_result"
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "output_video.mp4")

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = None

print("\n YOLO Face + Recognition Running...\n")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    display = frame.copy()

    # YOLO FACE DETECTION
    boxes = face_detector.detect(frame)

    print("Detected faces:", len(boxes))

    for (x1, y1, x2, y2) in boxes:

        face_crop = frame[y1:y2, x1:x2]

        if face_crop.size == 0:
            continue

        #  RECOGNITION
        name = face_recognizer.recognize(face_crop)

        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)

        cv2.rectangle(display, (x1, y1), (x2, y2), color, 2)
        cv2.putText(display, name, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    if out is None:
        h, w = display.shape[:2]
        out = cv2.VideoWriter(output_path, fourcc, 20, (w, h))

    out.write(display)

    cv2.imshow("YOLO Face Recognition", display)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
if out:
    out.release()

cv2.destroyAllWindows()

print("Saved:", output_path)