import cv2
import numpy as np
from PIL import Image, ImageEnhance
import os

def adjust_hue_pil(image_path, hue_factor):
    img = Image.open(image_path)
    hsv = img.convert('HSV')

    hue = hsv.split()[0]
    hue = hue.point(lambda p: (p + hue_factor * 255) % 256)
    
    new_img = Image.merge('HSV', (hue, hsv.split()[1], hsv.split()[2]))
    return new_img.convert('RGB')

# Harus dalam bentuk float
brightness_value = float(input("Brightness value: "))
contrast_value = float(input("Contrast value: "))
hue_value = float(input("Hue value: "))
sat_value = float(input("Saturation value: "))

def adjustment(image_path, brightnessFac, contrastFac, hueFac, saturationFac):

    
    new_image = Image.open(image_path)
    temp_image_path = f"temp_{os.path.basename(image_path)}"
    print(image_path, ", Temp image:", temp_image_path)

    ################ BRIGHTNESS ################

    # Min 0, default 1, max 10
    brightnessFilter = ImageEnhance.Brightness(new_image)

    temp_edited_image = brightnessFilter.enhance(brightnessFac)
    temp_edited_image.save(temp_image_path)
    
    ################ CONTRAST ################
    
    # Min 0, default 1, max 10
    temp_new_image_contrast = Image.open(temp_image_path)

    contrastFilter = ImageEnhance.Contrast(temp_new_image_contrast)

    temp_edited_image = contrastFilter.enhance(contrastFac)
    temp_edited_image.save(temp_image_path)

    # ################ SATURATION ################

    temp_new_image_saturation = Image.open(temp_image_path)
    saturationFilter = ImageEnhance.Color(temp_new_image_saturation)

    temp_edited_image = saturationFilter.enhance(saturationFac)
    temp_edited_image.save(temp_image_path)

    # ############### HUE COLOR ################

    temp_new_image_hue = adjust_hue_pil(temp_image_path, hueFac)
    temp_new_image_hue.save("output.jpg")


    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    os.remove(temp_image_path)

adjustment("sample.jpg", brightness_value, contrast_value, hue_value, sat_value)
