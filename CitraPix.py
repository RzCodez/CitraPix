from flask import Flask, render_template, request

app = Flask(__name__, static_folder="./static", template_folder="./templates")

@app.route("/")
def home():
    return render_template("index.html", testing_content="Ini saya upload via vercel, doakan saya berhasil!")

@app.route("/deblurring")
def deblurring():
    return render_template("deblurring.html")

if __name__ == '__main__':
    app.run()


