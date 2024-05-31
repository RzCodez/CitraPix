import cv2
import numpy as np
import matplotlib.pyplot as plt

def create_disk_kernel(radius):
    """Membuat kernel berbentuk disk untuk efek lens blur."""
    L = np.arange(-radius, radius+1)
    X, Y = np.meshgrid(L, L)
    kernel = np.sqrt(X**2 + Y**2) <= radius
    return kernel.astype(np.float32)

def apply_lens_blur(image_path, radius):
    image = cv2.imread(image_path)

    # image = np.float32(image_path) / 255.0

    disk_kernel = create_disk_kernel(radius)
    disk_kernel /= np.sum(disk_kernel)

    blurred_image = cv2.filter2D(image, -1, disk_kernel)
    return blurred_image
