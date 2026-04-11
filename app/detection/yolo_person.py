
from ultralytics import YOLO

class PersonDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect(self, frame):
    
        results = self.model(frame, verbose=False)

        persons = []

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])

                if cls == 0:  # person
                    persons.append({
                        "id": -1,  # placeholder (we'll fix later with ByteTrack)
                        "bbox": box.xyxy[0].tolist(),
                        "confidence": float(box.conf[0])
                    })

        return persons