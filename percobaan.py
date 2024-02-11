import cv2
import numpy as np

image = cv2.imread("sample_3.jpg")

gaussian_blur = cv2.GaussianBlur(image,(13,13),3)

# sharpened = cv2.addWeighted(image, 1.5, gaussian_blur, -0.5, 0)
# smooth = cv2.blur(sharpened,(5,5), 0)
cv2.imshow('Gaussian',gaussian_blur)
cv2.imshow('Original',image)
# cv2.imshow('Sharpened',sharpened)
# cv2.imshow('Smooth',smooth)
cv2.waitKey(0)
