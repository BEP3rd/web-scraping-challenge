from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo  = PyMongo(app, uri="mongodb://localhost:27017/Mars_DB")

@app.route("/")
def index():
    app_data = mongo.db.collection.find_one()
    return render_template("index.html", data = app_data)

@app.route("/scrape")
def scrape():
    
    mongo.db.collection.drop()
    mars_data = scrape_mars.scrape_all()
    mongo.db.collection.insert_one(mars_data)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)