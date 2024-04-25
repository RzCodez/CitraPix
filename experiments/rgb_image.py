from PIL import Image
import matplotlib.pyplot as plt
import cv2
import numpy as np

###############################################
#                                             #
#               USER ENTRIES                  #
#                                             #
###############################################

merah = int(input("Merah value: "))
hijau = int(input("Hijau value: "))
biru = int(input("Biru value: "))

###############################################
#                                             #
#                PREPARATION                  #
#                                             #
###############################################

image = Image.open("sample.jpg")
image = image.convert("RGB")
width, height = image.size

for y in range(height):
    for x in range(width):
        r, g, b = image.getpixel((x, y))

        r_new = min(255, r + merah)
        g_new = min(255, g + hijau)
        b_new = min(255, b + biru)

        image.putpixel((x, y), (r_new, g_new, b_new))

image.save("output.jpg")
cv2.imwrite("output.jpg", cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR))

###############################################
#                                             #
#                MAIN PROGRAM                 #
#                                             #
###############################################

# output = cv2.imread("output.jpg")
# output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)

# plt.imshow(output)
# plt.show()