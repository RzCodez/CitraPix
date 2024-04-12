```py
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np

app = Flask(__name__, static_folder="./static", template_folder="./templates")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/deblurring", methods=["GET", "POST"])  
def deblurring():
    if request.method == "POST":

        gaussian_blur = request.form.get("gaussian")
        motion_blur = request.form.get("motion")
        lens_blur = request.form.get("lensblur")

        print("Gaussian Blur:", gaussian_blur)
        print("Motion Blur:", motion_blur)
        print("Lens Blur:", lens_blur)

        if(gaussian_blur):

            return render_template("deblurring.html", result="Gaussian Blur", gaussian=gaussian_blur)
        if(motion_blur):
            return render_template("deblurring.html", result="Motion Blur")
        if(lens_blur):
            return render_template("deblurring.html", result="Lens Blur")
        
        return redirect(url_for("home"))
    
    # Jika metode adalah GET, tampilkan halaman deblurring.html seperti biasa
    return render_template("deblurring.html")
    
```