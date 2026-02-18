import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form["query"]

        url = f"https://www.google.com/search?q={query}&tbm=isch"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        images = soup.find_all("img")

        save_dir = "static/images"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        count = 0
        for img in images:
            img_url = img.get("src")

            if img_url and img_url.startswith("http"):
                try:
                    img_data = requests.get(img_url).content
                    with open(os.path.join(save_dir, f"{query}_{count}.jpg"), "wb") as f:
                        f.write(img_data)
                    count += 1
                except:
                    pass

        return render_template("result.html", query=query, count=count)


    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
