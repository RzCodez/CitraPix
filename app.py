"""
PR IMAGE PROCESSING
1. Bisa memilih area yang mana ingin diapply
2. Object Detection

"""


from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import subprocess

# LIBRARY FILE SENDIRI
from facial_landmarks import FaceLandmarks
from blur_function import lensblur


app = Flask(__name__, static_folder="./static", template_folder="./templates")

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def adjust_hue_pil(image_path, hue_factor):
    img = Image.open(image_path)
    hsv = img.convert('HSV')

    hue = hsv.split()[0]
    hue = hue.point(lambda p: (p + hue_factor * 255) % 256)
    
    new_img = Image.merge('HSV', (hue, hsv.split()[1], hsv.split()[2]))
    return new_img.convert('RGB')

def motion_blur_effect(img, blur_length, angle):
    angle = float(angle)
    psf = np.zeros((50, 50, 3))
    psf = cv2.ellipse(psf, (25, 25), (blur_length, 0), angle, 0, 360, (1, 1, 1), thickness=-1)
    psf /= psf[:,:,0].sum() 
    imfilt = cv2.filter2D(img, -1, psf)
    return imfilt

# def lens_blur(img, blur_):


# def motion_blur_effect(img, blur_length, angle):
#     psf = np.zeros((50, 50, 3))
#     psf = cv2.ellipse(psf, 
#                     (25, 25),
#                     (blur_length, blur_length),
#                     angle,
#                     0, 360,
#                     (1, 1, 1),
#                     thickness=-1)

#     psf /= psf[:,:,0].sum() 

#     imfilt = cv2.filter2D(img, -1, psf)
#     return imfilt

# def motion_blur_effect(image, size, angle):
#     k = cv2.getGaussianKernel(size, -1)
#     psf = k @ k.T
#     center = (psf.shape[0] // 2, psf.shape[1] // 2)
#     rot_mat = cv2.getRotationMatrix2D(center, angle, 1.0)
#     psf = cv2.warpAffine(psf, rot_mat, (psf.shape[0], psf.shape[1]))
#     psf = psf / psf.sum()
#     blurred = cv2.filter2D(image, -1, psf)
#     return blurred

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/blur", methods=["GET", "POST"])  
def blurring():
    if request.method == "POST":
        if 'image' not in request.files:
            return redirect(request.url)

        file = request.files['image']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Mode blur
            gaussian_blur = request.form.get("gaussian")
            motion_blur_option = request.form.get("motion")
            lens_blur = request.form.get("lensblur")

            # Mode fokus muka
            face_detect_on = request.form.get("face-true")
            face_invert = request.form.get("invert")
            face_only = request.form.get("blurface")

            # KHUSUS MOTION BLUR
            angle = request.form.get("angle")
            radius = request.form.get("radius")




            fl = FaceLandmarks()


            image = cv2.imread(file_path)
            height, width, _ = image.shape

            if gaussian_blur:
                print("You've choosen Gaussian Blur!")
                print("Creating gaussian blur...")

                if face_detect_on:
                    
                    mask = np.zeros((height, width), np.uint8)

                    landmarks = fl.get_facial_landmarks(image)
                    convexhull = cv2.convexHull(landmarks)
                    cv2.fillConvexPoly(mask, convexhull, 255)

                    if face_only:
                        image_blur = cv2.GaussianBlur(image, (27, 27), 0) 
                        face_extracted = cv2.bitwise_and(image_blur, image_blur, mask=mask)
                        background_mask = cv2.bitwise_not(mask)
                        background = cv2.bitwise_and(image, image, mask=background_mask)
                        result = cv2.add(background, face_extracted)
                        cv2.imwrite(os.path.join(app.config["UPLOAD_FOLDER"], "blurred_" + filename), result)
                    
                    elif face_invert:
                        image_blur = cv2.GaussianBlur(image, (27, 27), 0)
                        face_without_blur = cv2.bitwise_and(image, image, mask=mask)
                        background_mask = cv2.bitwise_not(mask)
                        background_blur = cv2.bitwise_and(image_blur, image_blur, mask=background_mask)
                        result = cv2.add(background_blur, face_without_blur)
                        cv2.imwrite(os.path.join(app.config["UPLOAD_FOLDER"], "blurred_" + filename), result)
                else:
                    image_blur = cv2.GaussianBlur(image, (27, 27), 0)
                    cv2.imwrite(os.path.join(app.config["UPLOAD_FOLDER"], "blurred_" + filename), image_blur)

                return render_template("blur.html", result="Gaussian Blur", image="blurred_" + filename)

            if motion_blur_option:
                print("You've choosen Motion Blur!")
                print("Creating motion blur...")

                if face_detect_on:
                    
                    mask = np.zeros((height, width), np.uint8)

                    landmarks = fl.get_facial_landmarks(image)
                    convexhull = cv2.convexHull(landmarks)
                    cv2.fillConvexPoly(mask, convexhull, 255)

                    if face_only:
                        # image_blur = cv2.GaussianBlur(image, (27, 27), 0)
                        image_blur = motion_blur_effect(image, 50, angle)
                        face_extracted = cv2.bitwise_and(image_blur, image_blur, mask=mask)
                        background_mask = cv2.bitwise_not(mask)
                        background = cv2.bitwise_and(image, image, mask=background_mask)
                        result = cv2.add(background, face_extracted)
                        cv2.imwrite(os.path.join(app.config["UPLOAD_FOLDER"], "blurred_" + filename), result)
                    
                    elif face_invert:
                        # image_blur = cv2.GaussianBlur(image, (27, 27), 0)
                        image_blur = motion_blur_effect(image, 100, angle)
                        face_without_blur = cv2.bitwise_and(image, image, mask=mask)
                        background_mask = cv2.bitwise_not(mask)
                        background_blur = cv2.bitwise_and(image_blur, image_blur, mask=background_mask)
                        result = cv2.add(background_blur, face_without_blur)
                        cv2.imwrite(os.path.join(app.config["UPLOAD_FOLDER"], "blurred_" + filename), result)
                else:
                    # image_blur = cv2.GaussianBlur(image, (27, 27), 0)
                    image_blur = motion_blur_effect(image, 10000, angle)
                    cv2.imwrite(os.path.join(app.config["UPLOAD_FOLDER"], "blurred_" + filename), image_blur)

                return render_template("blur.html", result="Motion Blur", image="blurred_" + filename)

            if lens_blur:
                print("You've choosen Lens Blur!")
                print("Creating lens blur...")

                if face_detect_on:
                    
                    mask = np.zeros((height, width), np.uint8)

                    landmarks = fl.get_facial_landmarks(image)
                    convexhull = cv2.convexHull(landmarks)
                    cv2.fillConvexPoly(mask, convexhull, 255)

                    if face_only:
                        # image_blur = cv2.GaussianBlur(image, (27, 27), 0)
                        image_blur = lensblur.apply_lens_blur(file_path, int(radius)) # (image, radius)
                        face_extracted = cv2.bitwise_and(image_blur, image_blur, mask=mask)
                        background_mask = cv2.bitwise_not(mask)
                        background = cv2.bitwise_and(image, image, mask=background_mask)
                        result = cv2.add(background, face_extracted)
                        cv2.imwrite(os.path.join(app.config["UPLOAD_FOLDER"], "blurred_" + filename), result)
                    
                    elif face_invert:
                        # image_blur = cv2.GaussianBlur(image, (27, 27), 0)
                        image_blur = lensblur.apply_lens_blur(file_path, int(radius)) # (image, radius)
                        face_without_blur = cv2.bitwise_and(image, image, mask=mask)
                        background_mask = cv2.bitwise_not(mask)
                        background_blur = cv2.bitwise_and(image_blur, image_blur, mask=background_mask)
                        result = cv2.add(background_blur, face_without_blur)
                        cv2.imwrite(os.path.join(app.config["UPLOAD_FOLDER"], "blurred_" + filename), result)
                else:
                    # image_blur = cv2.GaussianBlur(image, (27, 27), 0)
                    image_blur = lensblur.apply_lens_blur(file_path, int(radius)) # (image, radius)
                    cv2.imwrite(os.path.join(app.config["UPLOAD_FOLDER"], "blurred_" + filename), image_blur)

                return render_template("blur.html", result="Lens Blur", image="blurred_" + filename)

    return render_template("blur.html")

@app.route("/rgb", methods=["GET", "POST"])
def rgb_img():
    if request.method == "POST":
        if 'image' not in request.files:
            return redirect(request.url)

        file = request.files['image']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            red = int(request.form.get("red"))
            green = int(request.form.get("green"))
            blue = int(request.form.get("blue"))

            image = Image.open(file_path)
            image = image.convert("RGB")
            width, height = image.size

            for y in range(height):
                for x in range(width):
                    r, g, b = image.getpixel((x, y))

                    r_new = min(255, r + red)
                    g_new = min(255, g + green)
                    b_new = min(255, b + blue)

                    image.putpixel((x, y), (r_new, g_new, b_new))

            cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], 'rgb_' + filename), cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR))

            return render_template("rgb.html", image=filename, image_output='rgb_' + filename)

            
    return render_template("rgb.html")


@app.route("/adjustment", methods=["GET", "POST"])
def adjustment():

    if request.method == "POST":
        if 'image' not in request.files:
            return redirect(request.url)

        file = request.files['image']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            #######################################################
            #                    USER ENTRIES                     #
            #######################################################

            new_image = Image.open(file_path)
            temp_image_path = f"temp_{filename}"

            brightness = request.form.get("brightness")
            contrast = request.form.get("contrast")
            hue = request.form.get("hue")
            saturation = request.form.get("saturation")

            brightnessFac = float(brightness)
            contrastFac = float(contrast)
            hueFac = float(hue)
            saturationFac = float(saturation)

            # MENGECEK APAKAH FILE BERHASIL DIUPLOAD
            print(file_path, ", Temp image:", temp_image_path)



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

            # Min 0, default 1, max 10
            temp_new_image_saturation = Image.open(temp_image_path)
            saturationFilter = ImageEnhance.Color(temp_new_image_saturation)

            temp_edited_image = saturationFilter.enhance(saturationFac)
            temp_edited_image.save(temp_image_path)

            # ############### HUE COLOR ################

            # Min 0, default 1, max 10
            temp_edited_image = adjust_hue_pil(temp_image_path, hueFac)

            cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], 'adjust_' + filename), cv2.cvtColor(np.array(temp_edited_image), cv2.COLOR_RGB2BGR))
            os.remove(temp_image_path)

            return render_template("adjustment.html", image=filename, image_output="adjust_" + filename)
    
    return render_template("adjustment.html")

@app.route("/sharp", methods=["GET", "POST"])
def sharp():
    if request.method == "POST":
        if 'image' not in request.files:
            return redirect(request.url)

        file = request.files['image']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            ########################################################
            #                     USER ENTRIES                     #
            ########################################################
            input_path = file_path
            output_path = f"temp_upscaled_{filename}"

            model_name = "realesrgan-x4plus-anime"

            command = ["realesrgan-ncnn-vulkan.exe", "-i", input_path, "-o", output_path, "-n", model_name]

            subprocess.run(command)
            upscaled_image = cv2.imread(output_path)

            cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], 'upscaled_' + filename), upscaled_image)


            os.remove(output_path)

            return render_template("sharp.html", image=filename, image_output="upscaled_" + filename)





    return render_template("sharp.html")


if __name__ == "__main__":
    app.run(debug=True)
