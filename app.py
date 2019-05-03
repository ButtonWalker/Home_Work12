# Import Dependencies 
from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars
import os


# Hidden authetication file
#import config 

# Create an instance of Flask app
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars_app")

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home(): 

    # Find data
    marsInfo = mongo.db.collection.find_one()
    # Return template and data
    return render_template("index.html", marsInfo=marsInfo)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run scrapped functions
    marsInfo = mongo.db.collection
    marsData = scrape_mars.scrapeMarsNews()
    marsData = scrape_mars.scrapeMarsImage()
    marsData = scrape_mars.scrapeMarsFacts()
    marsData = scrape_mars.scrapeMarsWeather()
    marsData = scrape_mars.scrapeMarsHemispheres()
    marsInfo.update({}, marsData, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)