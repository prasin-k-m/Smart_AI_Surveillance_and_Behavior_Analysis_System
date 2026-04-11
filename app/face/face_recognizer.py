
import face_recognition
import os
import numpy as np

class FaceRecognizer:
    def __init__(self, known_faces_dir, tolerance=0.6):  # Controls matching strictness
        self.known_encodings = []                        # Stores face features (numerical vectors)
        self.known_names = []                            # Stores names (from filenames)
        self.tolerance = tolerance

        print("Loading known faces...")

        for file in os.listdir(known_faces_dir):
            path = os.path.join(known_faces_dir, file)  

            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)   # Extracts face encoding

            if len(encodings) == 0:       
                print(f"No face found in: {file}")
                continue

            self.known_encodings.append(encodings[0])
            self.known_names.append(os.path.splitext(file)[0])

            print(f" Loaded: {self.known_names[-1]}")

        # IMPORTANT FIX
        if len(self.known_encodings) == 0:
            print(" No valid faces loaded. Recognition will return 'Unknown'.")

    def recognize(self, face_image):
        # prevent crash when no known faces
        if len(self.known_encodings) == 0:
            return "Unknown"

        encodings = face_recognition.face_encodings(face_image)

        if len(encodings) == 0:
            return "Unknown"

        # encoding = encodings[0]

        # distances = face_recognition.face_distance(self.known_encodings, encoding)

        # if len(distances) == 0:
        #     return "Unknown"

        # best_match_index = np.argmin(distances)

        # if distances[best_match_index] < self.tolerance:
        #     return self.known_names[best_match_index]

        # return "Unknown"
        


        results = []

        for encoding in encodings:
            distances = face_recognition.face_distance(self.known_encodings, encoding)    # similarity

            if len(distances) == 0:
                results.append("Unknown")
                continue

            best_match_index = np.argmin(distances)

            if distances[best_match_index] < self.tolerance:
                results.append(self.known_names[best_match_index])
            else:
                results.append("Unknown")

        return results