import cv2
import numpy as np

sharpening_kernel =  np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]
])
image = cv2.imread("sample_3.jpg")
sharpened = cv2.filter2D(image,-1,sharpening_kernel)
gaussian_blur = cv2.GaussianBlur(image,(7,7),3)

merge_smooth_image = cv2.addWeighted(gaussian_blur,0.5,sharpened,0.5,0)

cv2.imshow('Original',image)
cv2.imshow('Gaussian',gaussian_blur)
cv2.imshow('Sharpened',sharpened)
cv2.imshow('Merge',merge_smooth_image)
cv2.waitKey(0)