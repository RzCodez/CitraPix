import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter


# user entries

upscale = int(input("Upscale value: "))

# Open an image
image = Image.open("sample_3.jpg")

image_resize = image.resize((image.width * upscale, image.height * upscale))
smooth_image = image_resize.filter(ImageFilter.SMOOTH)
# Apply a sharpening filter
sharpened_image = smooth_image.filter(ImageFilter.SHARPEN)
two_x_sharpened_image = sharpened_image.filter(ImageFilter.SHARPEN)

sharpened_image.show()
two_x_sharpened_image.show()

# fig, (ax3, ax4) = plt.subplots(1, 2, figsize=(15, 3))

# ax1.imshow(image)
# ax1.set_title('Original')

# ax2.imshow(sharpened_image)
# ax2.set_title('Sharpened')

# ax3.imshow(sharpened_image)
# ax3.set_title('2x Sharpened')

# ax4.imshow(two_x_sharpened_image)
# ax4.set_title('2x Sharpened + smooth')


plt.tight_layout()
plt.show()


# Save or display the sharpened image
# sharpened_image.save("sharpened_example.jpg")
# image.show()
# sharpened_image.show()


