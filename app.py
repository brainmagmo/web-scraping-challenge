from flask import Flask, render_template
import pymongo
from scrape_mars import scrape

app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"

@app.route("/")
def index():
	client = pymongo.MongoClient(conn)
	db = client.mars
	data = db.data
	return render_template("index.html", mars_data = data.find_one())
	
@app.route("/scrape")
def scrape_page():
	new_data = scrape()
	
	client = pymongo.MongoClient(conn)
	db = client.mars
	data = db.data
	data.update({}, new_data, upsert=True)
	return redirect("/", code=302)
	


if __name__ == "__main__":
    app.run(debug=True)
	