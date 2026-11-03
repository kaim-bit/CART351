from flask import Flask, render_template, request, redirect, url_for
import requests
app = Flask(__name__)


# the default route
@app.route("/")
def index():
      return render_template("index.html")


#*************************************************
#Task-1: GET REQUEST
@app.route("/t1")
def t1():
    return render_template("t1.html", have_results=False)
#*************************************************
@app.route("/getSearchCriteria")
def getSearchCriteria():
    search_term = request.args.get("Input", "").strip()
    response = requests.get(
        "https://images-api.nasa.gov/search",
        params={"q": search_term, "media_type": "image"}
    )
    nasaImages = response.json()["collection"]["items"]

    if nasaImages:
        first_image = nasaImages[0]
        description = first_image["data"][0].get(
            "description"
        )
        img_path = first_image["links"][0]["href"]
        return render_template(
            "t1.html",
            have_results=True,
            description=description,
            imgPath=img_path
        )
    pass

#*************************************************
# #Task-2: GET REQUEST
@app.route("/t2")
def t2():
    return render_template("t2.html", images=[])
#*************************************************
@app.route("/getSearchCriteria_adv")
def getSearchCriteria_adv():
    search_term = request.args.get("Input", "").strip()

    response = requests.get(
        "https://images-api.nasa.gov/search",
        params={"q": search_term, "media_type": "image"}
    )
    data = response.json()
    nasaImages= data["collection"]["items"]
    encodedImageLinks = []

    for item in nasaImages:
        singleImage = item["links"][0]["href"]
        singleImage = singleImage.replace(" ", "%20")
        encodedImageLinks.append(singleImage)

    return render_template(
        "t2.html",
        images=encodedImageLinks,
        search_term=search_term
    )
#*************************************************

#run
app.run(debug=True)