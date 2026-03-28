# # # # # import cv2
# # # # # from app.face.face_recognizer import FaceRecognizer

# # # # # recognizer = FaceRecognizer("Sample_data/Known_faces/Images")

# # # # # cap = cv2.VideoCapture(0)  # or video path

# # # # # print("\n🚀 Face Recognition Started...\n")

# # # # # while True:
# # # # #     ret, frame = cap.read()
# # # # #     if not ret:
# # # # #         break

# # # # #     faces = recognizer.recognize(frame)

# # # # #     for face in faces:
# # # # #         x1, y1, x2, y2 = face["bbox"]
# # # # #         name = face["name"]

# # # # #         cv2.rectangle(frame, (x1,y1), (x2,y2), (255,0,0), 2)
# # # # #         cv2.putText(frame, name, (x1,y1-10),
# # # # #                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)

# # # # #     cv2.imshow("DLIB Face Recognition", frame)

# # # # #     if cv2.waitKey(1) == 27:
# # # # #         break

# # # # # cap.release()
# # # # # cv2.destroyAllWindows()

# # # # import cv2
# # # # import os
# # # # from app.face.face_recognizer import FaceRecognizer

# # # # recognizer = FaceRecognizer("Sample_data/Known_faces/Images")

# # # # # ❌ OLD webcam
# # # # # cap = cv2.VideoCapture(0)

# # # # # ✅ Video input
# # # # video_path = r"Sample_data/Known_faces/video/face.mp4"
# # # # cap = cv2.VideoCapture(video_path)

# # # # if not cap.isOpened():
# # # #     print("❌ Cannot open video")
# # # #     exit()

# # # # # ✅ Output folder
# # # # output_dir = "Outputs/face_result"
# # # # os.makedirs(output_dir, exist_ok=True)

# # # # output_path = os.path.join(output_dir, "output_video.avi")

# # # # # ✅ Fixed resolution
# # # # frame_width = 640
# # # # frame_height = 480
# # # # fps = 25

# # # # fourcc = cv2.VideoWriter_fourcc(*'XVID')
# # # # out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# # # # print("\n🚀 Face Recognition Started on Video...\n")

# # # # while True:
# # # #     ret, frame = cap.read()

# # # #     if not ret:
# # # #         break

# # # #     # ✅ Resize frame BEFORE recognition
# # # #     frame = cv2.resize(frame, (frame_width, frame_height))

# # # #     try:
# # # #         faces = recognizer.recognize(frame)
# # # #     except Exception as e:
# # # #         print("❌ Recognition error:", e)
# # # #         faces = []

# # # #     for face in faces:
# # # #         x1, y1, x2, y2 = face["bbox"]
# # # #         name = face["name"]

# # # #         cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
# # # #         cv2.putText(frame, name, (x1, y1 - 10),
# # # #                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

# # # #     out.write(frame)

# # # #     # Optional display
# # # #     try:
# # # #         cv2.imshow("Face Recognition", frame)
# # # #         if cv2.waitKey(1) & 0xFF == 27:
# # # #             break
# # # #     except:
# # # #         pass

# # # # cap.release()
# # # # out.release()
# # # # cv2.destroyAllWindows()

# # # # print(f"\n✅ Output saved at: {output_path}")
# # # import cv2
# # # import os
# # # from app.face.face_recognizer import FaceRecognizer

# # # recognizer = FaceRecognizer("Sample_data/Known_faces/Images")

# # # # ❌ Webcam
# # # # cap = cv2.VideoCapture(0)

# # # # ✅ Video
# # # video_path = r"Sample_data/Known_faces/video/face.mp4"
# # # cap = cv2.VideoCapture(video_path)

# # # if not cap.isOpened():
# # #     print("❌ Cannot open video")
# # #     exit()

# # # output_dir = "Outputs/face_result"
# # # os.makedirs(output_dir, exist_ok=True)

# # # output_path = os.path.join(output_dir, "output_video.avi")

# # # frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# # # frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# # # fps = 25

# # # fourcc = cv2.VideoWriter_fourcc(*'XVID')
# # # out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# # # print("\n🚀 Face Recognition Started...\n")

# # # frame_count = 0
# # # faces = []

# # # while True:
# # #     ret, frame = cap.read()
# # #     if not ret:
# # #         break

# # #     frame_count += 1

# # #     # ✅ Process every 2nd frame (smooth + fast)
# # #     if frame_count % 2 == 0:
# # #         try:
# # #             faces = recognizer.recognize(frame)
# # #         except Exception as e:
# # #             print("❌ Error:", e)

# # #     # Draw last detected faces (smooth tracking feel)
# # #     for face in faces:
# # #         x1, y1, x2, y2 = face["bbox"]
# # #         name = face["name"]

# # #         cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
# # #         cv2.putText(frame, name, (x1, y1 - 10),
# # #                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

# # #     out.write(frame)

# # #     cv2.imshow("Face Recognition", frame)

# # #     # ✅ Smooth playback
# # #     if cv2.waitKey(30) & 0xFF == 27:
# # #         break

# # # cap.release()
# # # out.release()
# # # cv2.destroyAllWindows()

# # # print(f"\n✅ Output saved at: {output_path}")



# # import cv2
# # import os
# # from app.face.face_recognizer import FaceRecognizer

# # # ✅ Set tolerance here
# # recognizer = FaceRecognizer("Sample_data/Known_faces/Images", tolerance=0.7)

# # # cap = cv2.VideoCapture(0)

# # video_path = r"Sample_data/Known_faces/video/face.mp4"
# # cap = cv2.VideoCapture(video_path)

# # if not cap.isOpened():
# #     print("❌ Cannot open video")
# #     exit()

# # output_dir = "Outputs/face_result"
# # os.makedirs(output_dir, exist_ok=True)

# # output_path = os.path.join(output_dir, "output_video.avi")

# # frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# # frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# # fps = 25

# # fourcc = cv2.VideoWriter_fourcc(*'XVID')
# # out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# # print("\n🚀 Face Recognition Started...\n")

# # frame_count = 0
# # faces = []

# # while True:
# #     ret, frame = cap.read()
# #     if not ret:
# #         break

# #     frame_count += 1

# #     if frame_count % 2 == 0:
# #         try:
# #             faces = recognizer.recognize(frame)
# #         except Exception as e:
# #             print("❌ Error:", e)

# #     for face in faces:
# #         x1, y1, x2, y2 = face["bbox"]
# #         name = face["name"]

# #         cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
# #         cv2.putText(frame, name, (x1, y1 - 10),
# #                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

# #     out.write(frame)

# #     cv2.imshow("Face Recognition", frame)

# #     if cv2.waitKey(30) & 0xFF == 27:
# #         break

# # cap.release()
# # out.release()
# # cv2.destroyAllWindows()

# # print(f"\n✅ Output saved at: {output_path}")








# #    some frame issue

# import cv2
# import os
# from app.face.face_recognizer import FaceRecognizer

# recognizer = FaceRecognizer("Sample_data/Known_faces/Images", tolerance=0.6)

# video_path = r"Sample_data/Known_faces/video/face.mp4"
# cap = cv2.VideoCapture(video_path)

# if not cap.isOpened():
#     print("❌ Cannot open video")
#     exit()

# # 🔥 Output setup
# output_dir = "Outputs/face_result"
# os.makedirs(output_dir, exist_ok=True)

# output_path = os.path.join(output_dir, "output_video.mp4")

# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = None

# print("\n🚀 Face Recognition Running...\n")

# frame_count = 0
# faces = []

# while True:
#     ret, frame = cap.read()

#     if not ret:
#         print("✅ Video finished")
#         break

#     frame_count += 1

#     display = frame.copy()

#     # 🔥 Run face detection every 10 frames
#     if frame_count % 10 == 0:
#         try:
#             faces = recognizer.recognize(frame)
#             print(f"Detected faces: {len(faces)}")
#         except Exception as e:
#             print("Error:", e)
#             faces = []

#     # Draw results
#     for face in faces:
#         x1, y1, x2, y2 = face["bbox"]
#         name = face["name"]

#         color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)

#         cv2.rectangle(display, (x1, y1), (x2, y2), color, 2)
#         cv2.putText(display, name, (x1, y1 - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

#     # 🔥 Initialize writer once
#     if out is None:
#         h, w = display.shape[:2]
#         out = cv2.VideoWriter(output_path, fourcc, 20, (w, h))

#     # 🔥 Save frame
#     out.write(display)

#     # 🔥 Show video
#     cv2.imshow("Face Recognition", display)

#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# cap.release()

# if out:
#     out.release()

# cv2.destroyAllWindows()

# print(f"\n✅ Output saved at: {output_path}")


import cv2
import os
from app.face.face_recognizer import FaceRecognizer
from app.face.face_detector import FaceDetector

# 🔥 USE YOLO FACE MODEL HERE
face_detector = FaceDetector("models/yolov8n-face.pt")
face_recognizer = FaceRecognizer("Sample_data/Known_faces/Images", tolerance=0.6)

video_path = r"Sample_data/Known_faces/video/face.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("❌ Cannot open video")
    exit()

output_dir = "Outputs/face_result"
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "output_video.mp4")

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = None

print("\n🚀 YOLO Face + Recognition Running...\n")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    display = frame.copy()

    # 🔥 YOLO FACE DETECTION
    boxes = face_detector.detect(frame)

    print("Detected faces:", len(boxes))

    for (x1, y1, x2, y2) in boxes:

        face_crop = frame[y1:y2, x1:x2]

        if face_crop.size == 0:
            continue

        # 🔥 RECOGNITION
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