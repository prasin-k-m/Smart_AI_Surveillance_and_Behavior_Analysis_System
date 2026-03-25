import mediapipe as mp
import cv2

class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose

    def process(self, frame):
        if frame is None or frame.size == 0:
            return None

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 🔥 FRESH MODEL EVERY CALL (CRITICAL FIX)
        with self.mp_pose.Pose(
            static_image_mode=True,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=0.5
        ) as pose:

            results = pose.process(rgb)

        return results


def detect_posture(landmarks, height, width):

    if landmarks is None:
        return "UNKNOWN"

    try:
        nose = landmarks.landmark[0]
        left_shoulder = landmarks.landmark[11]
        right_shoulder = landmarks.landmark[12]
        left_hip = landmarks.landmark[23]
        right_hip = landmarks.landmark[24]
        left_knee = landmarks.landmark[25]
        right_knee = landmarks.landmark[26]

        nose_y = nose.y * height
        shoulder_y = ((left_shoulder.y + right_shoulder.y) / 2) * height
        hip_y = ((left_hip.y + right_hip.y) / 2) * height
        knee_y = ((left_knee.y + right_knee.y) / 2) * height

        if abs(shoulder_y - hip_y) < 40:
            return "FALL"

        if shoulder_y < nose_y < hip_y:
            return "BENDING"

        if abs(hip_y - knee_y) < 40:
            return "SITTING"

        if nose_y < shoulder_y < hip_y:
            return "STANDING"

    except:
        return "UNKNOWN"

    return "UNKNOWN"