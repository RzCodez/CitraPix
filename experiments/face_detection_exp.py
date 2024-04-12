import cv2
import numpy as np
from facial_landmarks import FaceLandmarks
import time

# Load face landmarks
fl = FaceLandmarks()

# Load image
image = cv2.imread("foto-sample-8.jpg")
height, width, _ = image.shape

# Input user
pilihan = input("Mau blur wajah atau tidak? (y/n) : ")

# Inisialisasi mask
mask = np.zeros((height, width), np.uint8)

# Deteksi wajah
landmarks = fl.get_facial_landmarks(image)
convexhull = cv2.convexHull(landmarks)
cv2.fillConvexPoly(mask, convexhull, 255)

print("Mendeteksi wajah...")
time.sleep(3)

if pilihan == "y":
    # Blur wajah
    image_blur = cv2.GaussianBlur(image, (27, 27), 0)  # Gunakan Gaussian Blur untuk menghaluskan tepi
    face_extracted = cv2.bitwise_and(image_blur, image_blur, mask=mask)
    background_mask = cv2.bitwise_not(mask)
    background = cv2.bitwise_and(image, image, mask=background_mask)
    result = cv2.add(background, face_extracted)
else:
    # Blur seluruh gambar kecuali wajah
    image_blur = cv2.blur(image, (27, 27))
    face_without_blur = cv2.bitwise_and(image, image, mask=mask)
    background_mask = cv2.bitwise_not(mask)
    background_blur = cv2.bitwise_and(image_blur, image_blur, mask=background_mask)
    result = cv2.add(background_blur, face_without_blur)

# Simpan gambar
print("Udah jadi, simpan gambar...")
time.sleep(2)
cv2.imwrite("output.png", result)
