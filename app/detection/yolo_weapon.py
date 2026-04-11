
from ultralytics import YOLO

class WeaponDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)


    def detect(self, frame, conf=0.55):   # default = 0.55
        results = self.model(frame, conf=conf, verbose=False)

        detections = []

        for r in results:
            for box in r.boxes:
                confidence = float(box.conf[0])
                cls = int(box.cls[0])

                detections.append({
                    "bbox": box.xyxy[0].tolist(),
                    "confidence": confidence,
                    "label": f"weapon_{cls}"   })
        return detections