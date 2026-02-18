import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
}

# ---------------- HOME PAGE ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form["query"]

        url = f"https://www.google.com/search?q={query}&tbm=isch"
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "html.parser")
        images = soup.find_all("img")

        save_dir = "static/images"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        count = 0
        for img in images:
            img_url = img.get("src")

            # agar src empty ho to data-src check karo
            if not img_url:
                img_url = img.get("data-src")

            if img_url and img_url.startswith("http"):
                try:
                    img_data = requests.get(img_url, headers=headers).content
                    filename = f"{query}_{count}.jpg"

                    with open(os.path.join(save_dir, filename), "wb") as f:
                        f.write(img_data)

                    count += 1
                except Exception as e:
                    print("Error downloading image:", e)

        return render_template("result.html", query=query, count=count)

    return render_template("index.html")


# ---------------- API ROUTE ----------------
@app.route("/api/scrape", methods=["POST"])
def api_scrape():
    data = request.get_json()
    query = data["query"]

    url = f"https://www.google.com/search?q={query}&tbm=isch"
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    images = soup.find_all("img")

    save_dir = "static/images"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    image_files = []
    count = 0

    for img in images:
        img_url = img.get("src")

        if not img_url:
            img_url = img.get("data-src")

        if img_url and img_url.startswith("http"):
            try:
                img_data = requests.get(img_url, headers=headers).content
                filename = f"{query}_{count}.jpg"

                with open(os.path.join(save_dir, filename), "wb") as f:
                    f.write(img_data)

                image_files.append(filename)
                count += 1
            except Exception as e:
                print("Error downloading image:", e)

    return jsonify({
        "query": query,
        "total_images": count,
        "files": image_files
    })


if __name__ == "__main__":
    app.run(debug=True)
