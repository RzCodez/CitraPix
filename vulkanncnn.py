import cv2
from PIL import Image
import subprocess

input_path = "sample.jpg"
output_path = "output_sample.jpg"

option = int(input("Gambar yang dipilih:\n1. Gambar Anime\n2. Gambar Real Life\nMasukkan pilihan: "))
model_name = "realesrgan-x4plus-anime"

command = ["realesrgan-ncnn-vulkan.exe", "-i", input_path, "-o", output_path, "-n", model_name]
subprocess.run(command)

