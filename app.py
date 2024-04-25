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
from facial_landmarks import FaceLandmarks
from PIL import Image

app = Flask(__name__, static_folder="./static", template_folder="./templates")

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            motion_blur = request.form.get("motion")
            lens_blur = request.form.get("lensblur")

            # Mode fokus muka
            face_detect_on = request.form.get("face-true")
            face_invert = request.form.get("invert")
            face_only = request.form.get("blurface")

            fl = FaceLandmarks()

            image = cv2.imread(file_path)
            height, width, _ = image.shape

            mask = np.zeros((height, width), np.uint8)

            landmarks = fl.get_facial_landmarks(image)
            convexhull = cv2.convexHull(landmarks)
            cv2.fillConvexPoly(mask, convexhull, 255)

            if gaussian_blur:
                print("You've choosen Gaussian Blur!")
                print("Creating gaussian blur...")

                if face_detect_on:

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

            if motion_blur:
                print("You've choosen motion blur!")
                print("Creating motion blur...")
                return render_template("blur.html", result="Motion Blur")

            if lens_blur:
                # Apply lens blur here

                return render_template("blur.html", result="Lens Blur")

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

            # print(red, green, blue)

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
            
            # image.save('rgb_' + filename)
            # cv2.imwrite('rgb_' + filename, cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR))
            cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], 'rgb_' + filename), cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR))

            return render_template("rgb.html", image=filename, image_output='rgb_' + filename)

            
    return render_template("rgb.html")


@app.route("/adjustment", methods=["GET", "POST"])
def adjustment():
    
    
    return render_template("adjustment.html")


if __name__ == "__main__":
    app.run(debug=True)
