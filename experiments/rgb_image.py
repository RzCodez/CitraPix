from PIL import Image

# Baca gambar
image = Image.open("sample.jpg")

# Ubah mode gambar ke "RGB" (jika tidak sudah)
image = image.convert("RGB")

# Ukuran gambar
width, height = image.size

# Ubah setiap pixel dalam gambar
for y in range(height):
    for x in range(width):
        # Dapatkan nilai RGB pixel saat ini
        r, g, b = image.getpixel((x, y))
        
        # # Cetak nilai RGB
        # print(f"Nilai RGB pada piksel ({x}, {y}):")
        # print("Red:", r)
        # print("Green:", g)
        # print("Blue:", b)

        # Manipulasi nilai RGB
        r_new = 19
        g_new = 60
        b_new = 255

        # Atur nilai RGB pixel saat ini
        image.putpixel((x, y), (r_new, g_new, b_new))

# # Simpan gambar yang telah dimanipulasi
# image.save("output.jpg")
