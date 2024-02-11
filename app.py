from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_folder="./static", template_folder="./templates")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/deblurring")
def deblurring():
    return render_template("deblurring.html")

# @app.route("/redirect-deblurring")
# def redirect_deblurring():
#     return redirect(url_for("deblurring"))