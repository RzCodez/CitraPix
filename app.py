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

            # Load image
            image = cv2.imread(file_path)
            height, width, _ = image.shape

            # Inisialisasi mask
            mask = np.zeros((height, width), np.uint8)

            # Deteksi wajah
            landmarks = fl.get_facial_landmarks(image)
            convexhull = cv2.convexHull(landmarks)
            cv2.fillConvexPoly(mask, convexhull, 255)

            if gaussian_blur:
                print("You've choosen Gaussian Blur!")
                print("Creating gaussian blur...")

                if face_detect_on:

                    if face_only:
                        image_blur = cv2.GaussianBlur(image, (27, 27), 0)  # Gunakan Gaussian Blur untuk menghaluskan tepi
                        face_extracted = cv2.bitwise_and(image_blur, image_blur, mask=mask)
                        background_mask = cv2.bitwise_not(mask)
                        background = cv2.bitwise_and(image, image, mask=background_mask)
                        result = cv2.add(background, face_extracted)
                        cv2.imwrite(os.path.join(app.config["UPLOAD_FOLDER"], "blurred_" + filename), result)
                    
                    elif face_invert:
                        # Blur seluruh gambar kecuali wajah
                        image_blur = cv2.GaussianBlur(image, (27, 27), 0)  # Gunakan Gaussian Blur untuk menghaluskan tepi
                        face_without_blur = cv2.bitwise_and(image, image, mask=mask)
                        background_mask = cv2.bitwise_not(mask)
                        background_blur = cv2.bitwise_and(image_blur, image_blur, mask=background_mask)
                        result = cv2.add(background_blur, face_without_blur)
                        cv2.imwrite(os.path.join(app.config["UPLOAD_FOLDER"], "blurred_" + filename), result)
                else:
                    image_blur = cv2.GaussianBlur(image, (27, 27), 0)  # Gunakan Gaussian Blur untuk menghaluskan tepi
                    cv2.imwrite(os.path.join(app.config["UPLOAD_FOLDER"], "blurred_" + filename), image_blur)

                return render_template("blur.html", result="Gaussian Blur", image="blurred_" + filename)

            if motion_blur:
                # Apply motion blur here
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
            # filename = secure_filename(file.filename)
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
    return render_template("rgb.html")


if __name__ == "__main__":
    app.run(debug=True)
