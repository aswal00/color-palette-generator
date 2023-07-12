import os
import numpy as np
from flask import Flask, render_template, request
from PIL import Image
from sklearn.cluster import KMeans
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/files/"


@app.route("/", methods=["GET", "POST"])
def home():
    table = False
    if request.method == "POST":
        file = request.files["file-upload"]
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        img = Image.open(file_path)
        pixels = np.array(img).reshape(-1, 3)
        kmeans = KMeans(n_clusters=10)
        kmeans.fit(pixels)
        colors = kmeans.cluster_centers_
        common_clrs = kmeans.transform(pixels).sum(axis=1)
        sorted_colors = [color for _, color in sorted(zip(common_clrs, colors), key=lambda x: x[0], reverse=True)]
        hex_codes = [f"#{''.join([f'{int(channel):02X}' for channel in color])}" for color in sorted_colors]
        table = True
        os.remove(file_path)
        return render_template("index.html", table=table, hex_codes=hex_codes)
    return render_template("index.html", table=table)


if __name__ == "__main__":
    app.run(debug=True)


