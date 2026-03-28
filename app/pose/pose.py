import mediapipe as mp
import cv2
import numpy as np


class PoseDetector:
    def __init__(self):
        self.pose = mp.solutions.pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def process(self, frame):
        try:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return self.pose.process(rgb)
        except:
            return None


# ---------------- POSTURE DETECTION ----------------
def detect_posture(landmarks, h, w):
    try:
        def pt(i):
            lm = landmarks.landmark[i]
            return np.array([lm.x * w, lm.y * h])

        # Key points
        shoulder = (pt(11) + pt(12)) / 2
        hip = (pt(23) + pt(24)) / 2

        # BODY ORIENTATION
        vec = shoulder - hip
        angle = np.degrees(np.arctan2(vec[1], vec[0]))
        angle = abs(angle)

        vertical_angle = abs(90 - angle)

        # FALL vs STANDING
        if vertical_angle > 45:
            return "FALLEN"

        return "STANDING"

    except:
        return "STANDING"