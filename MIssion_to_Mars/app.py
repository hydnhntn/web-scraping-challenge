from flask import Flask, render_template

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Import custom scrape function
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.marsMission
col = db.mars

# set home route
@app.route('/')
def index():
    mars_data = col.find_one()
    return render_template('index.html',mars=mars_data)

# Set scrape route
@app.route('/scrape')
def scrape():

    mars_data = scrape_mars.scrape()
    col.update_one({}, {"$set": mars_data}, upsert=True)

    return "update successful!"


if __name__ == "__main__":
    app.run(debug=True)