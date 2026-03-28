from ultralytics import YOLO

class FaceDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(frame, verbose=False)

        faces = []

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                faces.append([int(x1), int(y1), int(x2), int(y2)])

        return faces