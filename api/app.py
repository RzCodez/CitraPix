from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np

app = Flask(__name__, static_folder="./static", template_folder="./templates")

@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/deblurring")
# def deblurring():
#     return render_template("deblurring.html")

@app.route("/deblurring", methods=["GET", "POST"])  
def deblurring():
    if request.method == "POST":
        input_image = request.files['input_image']

        input_image_path = os.path.join(app.config['UPLOAD_FOLDER'], input_image.filename)
        input_image.save(input_image_path)
        gaussian_blur = request.form.get("gaussian")
        motion_blur = request.form.get("motion")
        lens_blur = request.form.get("lensblur")

        print("Gaussian Blur:", gaussian_blur)
        print("Motion Blur:", motion_blur)
        print("Lens Blur:", lens_blur)
        print("Input Image:", input_image_path)

        image = cv2.imread(input_image_path)
        if(gaussian_blur):
            gaussian_blur = cv2.GaussianBlur(image,(7,7),3)
            return render_template("deblurring.html", result="Gaussian Blur", gaussian=gaussian_blur)
        if(motion_blur):
            return render_template("deblurring.html", result="Motion Blur")
        if(lens_blur):
            return render_template("deblurring.html", result="Lens Blur")
        
        return redirect(url_for("home"))
    
    # Jika metode adalah GET, tampilkan halaman deblurring.html seperti biasa
    return render_template("deblurring.html")
