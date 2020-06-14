# import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scraping

# set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# define the route to the html page
@app.route("/")
def index():
   mars = mongo.db.mars_app.find_one()
   return render_template("index.html", mars=mars) #list=hemi_titles)

# scrape route
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars_app
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   #return "Scraping Successful!" 
   return redirect("/")
   ## in index... make a button to redirect (above) to home page

if __name__ == "__main__":
   app.run(debug=True)