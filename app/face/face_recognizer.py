# # # # import face_recognition
# # # # import os

# # # # class FaceRecognizer:
# # # #     def __init__(self, known_faces_dir):
# # # #         self.known_encodings = []
# # # #         self.known_names = []

# # # #         print("🔄 Loading known faces...")

# # # #         for file in os.listdir(known_faces_dir):
# # # #             path = os.path.join(known_faces_dir, file)

# # # #             image = face_recognition.load_image_file(path)
# # # #             encodings = face_recognition.face_encodings(image)

# # # #             if len(encodings) > 0:
# # # #                 self.known_encodings.append(encodings[0])
# # # #                 name = os.path.splitext(file)[0]
# # # #                 self.known_names.append(name)

# # # #                 print(f"✅ Loaded: {name}")
# # # #             else:
# # # #                 print(f"⚠️ No face found in: {file}")

# # # #     def recognize(self, frame):
# # # #         rgb = frame[:, :, ::-1]

# # # #         face_locations = face_recognition.face_locations(rgb)
# # # #         face_encodings = face_recognition.face_encodings(rgb, face_locations)

# # # #         results = []

# # # #         for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):

# # # #             matches = face_recognition.compare_faces(self.known_encodings, encoding)
# # # #             name = "Unknown"

# # # #             if True in matches:
# # # #                 index = matches.index(True)
# # # #                 name = self.known_names[index]

# # # #             results.append({
# # # #                 "name": name,
# # # #                 "bbox": [left, top, right, bottom]
# # # #             })

# # # #         return results








# # # # import face_recognition
# # # # import os
# # # # import cv2
# # # # import numpy as np

# # # # class FaceRecognizer:
# # # #     def __init__(self, known_faces_dir):
# # # #         self.known_encodings = []
# # # #         self.known_names = []

# # # #         print("🔄 Loading known faces...")

# # # #         for file in os.listdir(known_faces_dir):
# # # #             path = os.path.join(known_faces_dir, file)

# # # #             image = face_recognition.load_image_file(path)
# # # #             encodings = face_recognition.face_encodings(image)

# # # #             if len(encodings) > 0:
# # # #                 self.known_encodings.append(encodings[0])
# # # #                 name = os.path.splitext(file)[0]
# # # #                 self.known_names.append(name)

# # # #                 print(f"✅ Loaded: {name}")
# # # #             else:
# # # #                 print(f"⚠️ No face found in: {file}")

# # # #     def recognize(self, frame):
# # # #         # ✅ Resize frame (VERY IMPORTANT)
# # # #         small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

# # # #         rgb = small_frame[:, :, ::-1]

# # # #         # ✅ Better detection model
# # # #         face_locations = face_recognition.face_locations(rgb, model="cnn")
# # # #         print("Detected faces:", len(face_locations))  # debug

# # # #         face_encodings = face_recognition.face_encodings(rgb, face_locations)

# # # #         results = []

# # # #         for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):

# # # #             name = "Unknown"

# # # #             if len(self.known_encodings) > 0:
# # # #                 # ✅ Best match logic
# # # #                 face_distances = face_recognition.face_distance(self.known_encodings, encoding)

# # # #                 best_match_index = np.argmin(face_distances)

# # # #                 if face_distances[best_match_index] < 0.6:
# # # #                     name = self.known_names[best_match_index]

# # # #             # ✅ Scale back coordinates
# # # #             top *= 2
# # # #             right *= 2
# # # #             bottom *= 2
# # # #             left *= 2

# # # #             results.append({
# # # #                 "name": name,
# # # #                 "bbox": [left, top, right, bottom]
# # # #             })

# # # #         return results









# # # import face_recognition
# # # import os
# # # import cv2
# # # import numpy as np

# # # class FaceRecognizer:
# # #     def __init__(self, known_faces_dir):
# # #         self.known_encodings = []
# # #         self.known_names = []

# # #         print("🔄 Loading known faces...")

# # #         for file in os.listdir(known_faces_dir):
# # #             path = os.path.join(known_faces_dir, file)

# # #             image = face_recognition.load_image_file(path)
# # #             encodings = face_recognition.face_encodings(image)

# # #             if len(encodings) > 0:
# # #                 self.known_encodings.append(encodings[0])
# # #                 name = os.path.splitext(file)[0]
# # #                 self.known_names.append(name)

# # #                 print(f"✅ Loaded: {name}")
# # #             else:
# # #                 print(f"⚠️ No face found in: {file}")

# # #     def recognize(self, frame):
# # #         small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
# # #         rgb = small_frame[:, :, ::-1]

# # #         face_locations = face_recognition.face_locations(rgb, model="cnn")
# # #         face_encodings = face_recognition.face_encodings(rgb, face_locations)

# # #         results = []

# # #         for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):

# # #             name = "Unknown"

# # #             if len(self.known_encodings) > 0:
# # #                 face_distances = face_recognition.face_distance(self.known_encodings, encoding)

# # #                 best_match_index = np.argmin(face_distances)

# # #                 # 🔥 CHANGED HERE (increase tolerance)
# # #                 if face_distances[best_match_index] < 0.75:
# # #                     name = self.known_names[best_match_index]

# # #                 # 🔍 Debug (optional)
# # #                 print(f"Distance: {face_distances[best_match_index]:.2f} -> {name}")

# # #             # Scale back
# # #             top *= 2
# # #             right *= 2
# # #             bottom *= 2
# # #             left *= 2

# # #             results.append({
# # #                 "name": name,
# # #                 "bbox": [left, top, right, bottom]
# # #             })

# # #         return results

# # import face_recognition
# # import os
# # import numpy as np
# # import cv2

# # class FaceRecognizer:
# #     def __init__(self, known_faces_dir):
# #         self.known_encodings = []
# #         self.known_names = []

# #         print("🔄 Loading known faces...")

# #         for file in os.listdir(known_faces_dir):
# #             path = os.path.join(known_faces_dir, file)

# #             image = face_recognition.load_image_file(path)

# #             face_locations = face_recognition.face_locations(image)

# #             if len(face_locations) == 0:
# #                 print(f"⚠️ No face found in: {file}")
# #                 continue

# #             encoding = face_recognition.face_encodings(image, face_locations)[0]

# #             self.known_encodings.append(encoding)
# #             name = os.path.splitext(file)[0]
# #             self.known_names.append(name)

# #             print(f"✅ Loaded: {name}")

# #     def recognize(self, frame):
# #         # ✅ Resize slightly (speed boost without losing detection)
# #         small_frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)
# #         rgb = small_frame[:, :, ::-1]

# #         # ✅ FAST detection (no freeze)
# #         face_locations = face_recognition.face_locations(rgb, model="hog")

# #         face_encodings = face_recognition.face_encodings(rgb, face_locations)

# #         results = []

# #         for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):

# #             name = "Unknown"

# #             if len(self.known_encodings) > 0:
# #                 face_distances = face_recognition.face_distance(self.known_encodings, encoding)
# #                 best_match_index = np.argmin(face_distances)

# #                 if face_distances[best_match_index] < 0.75:
# #                     name = self.known_names[best_match_index]

# #             # scale back
# #             scale = 1 / 0.75
# #             top = int(top * scale)
# #             right = int(right * scale)
# #             bottom = int(bottom * scale)
# #             left = int(left * scale)

# #             results.append({
# #                 "name": name,
# #                 "bbox": [left, top, right, bottom]
# #             })

# #         # return results







# ###   working- only  problem in some frame

# # import face_recognition
# # import os
# # import numpy as np
# # import cv2

# # class FaceRecognizer:
# #     def __init__(self, known_faces_dir, tolerance=0.6):
# #         self.known_encodings = []
# #         self.known_names = []
# #         self.tolerance = tolerance

# #         print("🔄 Loading known faces...")

# #         for file in os.listdir(known_faces_dir):
# #             path = os.path.join(known_faces_dir, file)

# #             image = face_recognition.load_image_file(path)
# #             encodings = face_recognition.face_encodings(image)

# #             if len(encodings) == 0:
# #                 print(f"⚠️ No face found in: {file}")
# #                 continue

# #             self.known_encodings.append(encodings[0])
# #             self.known_names.append(os.path.splitext(file)[0])

# #             print(f"✅ Loaded: {self.known_names[-1]}")

# #     def recognize(self, frame):
# #         # SMALL resize for speed
# #         small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
# #         rgb = small[:, :, ::-1]

# #         face_locations = face_recognition.face_locations(rgb)
# #         face_encodings = face_recognition.face_encodings(rgb, face_locations)

# #         results = []

# #         for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):

# #             name = "Unknown"

# #             if len(self.known_encodings) > 0:
# #                 distances = face_recognition.face_distance(self.known_encodings, encoding)
# #                 best_match_index = np.argmin(distances)

# #                 if distances[best_match_index] < self.tolerance:
# #                     name = self.known_names[best_match_index]

# #             # scale back
# #             top *= 2
# #             right *= 2
# #             bottom *= 2
# #             left *= 2

# #             results.append({
# #                 "name": name,
# #                 "bbox": [left, top, right, bottom]
# #             })

# #         return results


# import face_recognition
# import os
# import numpy as np

# class FaceRecognizer:
#     def __init__(self, known_faces_dir, tolerance=0.6):
#         self.known_encodings = []
#         self.known_names = []
#         self.tolerance = tolerance

#         print("🔄 Loading known faces...")

#         for file in os.listdir(known_faces_dir):
#             path = os.path.join(known_faces_dir, file)

#             image = face_recognition.load_image_file(path)
#             encodings = face_recognition.face_encodings(image)

#             if len(encodings) == 0:
#                 print(f"⚠️ No face found in: {file}")
#                 continue

#             self.known_encodings.append(encodings[0])
#             self.known_names.append(os.path.splitext(file)[0])

#             print(f"✅ Loaded: {self.known_names[-1]}")

#     def recognize(self, face_image):
#         encodings = face_recognition.face_encodings(face_image)

#         if len(encodings) == 0:
#             return "Unknown"

#         encoding = encodings[0]

#         distances = face_recognition.face_distance(self.known_encodings, encoding)
#         best_match_index = np.argmin(distances)

#         if distances[best_match_index] < self.tolerance:
#             return self.known_names[best_match_index]

#         return "Unknown"




import face_recognition
import os
import numpy as np

class FaceRecognizer:
    def __init__(self, known_faces_dir, tolerance=0.6):
        self.known_encodings = []
        self.known_names = []
        self.tolerance = tolerance

        print("🔄 Loading known faces...")

        for file in os.listdir(known_faces_dir):
            path = os.path.join(known_faces_dir, file)

            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)

            if len(encodings) == 0:
                print(f"⚠️ No face found in: {file}")
                continue

            self.known_encodings.append(encodings[0])
            self.known_names.append(os.path.splitext(file)[0])

            print(f"✅ Loaded: {self.known_names[-1]}")

        # ✅ IMPORTANT FIX
        if len(self.known_encodings) == 0:
            print("⚠️ No valid faces loaded. Recognition will return 'Unknown'.")

    def recognize(self, face_image):
        # ✅ FIX: prevent crash when no known faces
        if len(self.known_encodings) == 0:
            return "Unknown"

        encodings = face_recognition.face_encodings(face_image)

        if len(encodings) == 0:
            return "Unknown"

        encoding = encodings[0]

        distances = face_recognition.face_distance(self.known_encodings, encoding)

        if len(distances) == 0:
            return "Unknown"

        best_match_index = np.argmin(distances)

        if distances[best_match_index] < self.tolerance:
            return self.known_names[best_match_index]

        return "Unknown"