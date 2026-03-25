
from ultralytics import YOLO

class PersonDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model.track(frame, persist=True, verbose=False)

        persons = []

        for r in results:
            if r.boxes.id is None:
                continue

            for box, track_id in zip(r.boxes, r.boxes.id):
                cls = int(box.cls[0])

                if cls == 0:  # person class
                    persons.append({
                        "id": int(track_id),
                        "bbox": box.xyxy[0].tolist(),
                        "confidence": float(box.conf[0])
                    })

        return persons