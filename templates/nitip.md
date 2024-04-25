
src="{{ url_for('static', filename='uploads/' + image) }}"

{% if image %}
<img src="" alt="Uploaded Image" class="w-full h-full obj" />
{% endif %}

```py
@app.route("/rgb-config", methods=["GET", "POST"])
def rgb_config():

    image_upload = request.args.get('image')
    
    filename = image_upload
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_upload)
    image = Image.open(file_path)
    image = image.convert("RGB")
    width, height = image.size

    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
    
    r_input = request.form.get("red")
    g_input = request.form.get("green")
    b_input = request.form.get("blue")

    if request.method == "POST":
        if 'image' not in request.files:
            return redirect(request.url)


        file = request.files['image']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            file.save(file_path)

            for y in range(height):
                for x in range(width):
                    r, g, b = image.getpixel((x, y))

                    r_new = min(255, r + r_input)
                    g_new = min(255, g + g_input)
                    b_new = min(255, b + b_input)

                    image.putpixel((x, y), (r_new, g_new, b_new))
            
            image.save(image, os.path.join(app.config["UPLOAD_FOLDER"], "result_" + filename))
            return redirect(url_for("rgb_result", image_result = "result_" + filename))

    return render_template("rgb_config.html", image=image_upload, red = r, green = g, blue = b)
    
```