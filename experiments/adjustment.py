import cv2
import numpy as np
from PIL import Image, ImageEnhance

# Harus dalam bentuk float
brightness_value = float(input("Brightness value: "))

def brightess(new_image, factor):

    image = Image.open(new_image)

    filter = ImageEnhance.Brightness(image)
    edited_image = filter.enhance(factor)

    edited_image.save("output.jpg")
    img_read = cv2.imread("output.jpg")

    cv2.imshow("Edited", img_read)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

brightess("sample.jpg", brightness_value)
