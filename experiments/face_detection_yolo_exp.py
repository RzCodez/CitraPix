import cv2
import mediapipe as mp
from ultralytics import YOLO
import numpy as np
import time

# Load YOLO model for face detection
facemodel = YOLO('yolov8n-face.pt')

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

image = cv2.imread("sample_3.jpg")

faces = facemodel.predict(image, conf=0.40)

# Iterate through detected faces
for face in faces:
    parameters = face.boxes
    for box in parameters:
        x1, y1, x2, y2 = box.xyxy[0].int().tolist() 
    
    face_region = image[y1:y2, x1:x2]

    results = face_mesh.process(cv2.cvtColor(face_region, cv2.COLOR_BGR2RGB))

    # Check jika landmarks terdeteksi
    if results.multi_face_landmarks:
        print("Face terdeteksi, lagi ngebuat landmarks...")

        for face_landmarks in results.multi_face_landmarks:
            landmarks = []
            for landmark in face_landmarks.landmark:
                h, w, _ = face_region.shape
                x_landmark, y_landmark = int(landmark.x * w), int(landmark.y * h)
                landmarks.append((x_landmark, y_landmark))
            
            mask = np.zeros_like(face_region)
            pts = np.array(landmarks, np.int32)
            cv2.fillPoly(mask, [pts], (255, 255, 255))

            blurred_face = cv2.GaussianBlur(face_region, (31, 31), 0)
            
            image[y1:y2, x1:x2] = np.where(mask == 255, blurred_face, face_region)

time.sleep(1)
print("Udah jadi, simpen gambar...")
cv2.imwrite("output.png", image)

