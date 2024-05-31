import cv2
import numpy as np

img = cv2.imread("cover.png")

def motion_blur(img, blur_length, angle):
    psf = np.zeros((50, 50, 3))
    psf = cv2.ellipse(psf, 
                    (25, 25),
                    (blur_length, 0), 
                    angle,
                    0, 360,
                    (1, 1, 1),
                    thickness=-1)

    psf /= psf[:,:,0].sum() 

    imfilt = cv2.filter2D(img, -1, psf)
    return imfilt

blurred = motion_blur(img, 10000, 45)
cv2.imshow("motion_blur", blurred)
cv2.waitKey(0)
cv2.destroyAllWindows()