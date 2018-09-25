from flask import Flask, render_template, redirect
import pymongo
import scrape_mars
import pandas as pd

app = Flask(__name__)

# Create connection to MongoDB database `weather_db` and collection `forecasts`
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mission

# Create route that renders index.html template and finds documents from mongo
@app.route('/')
def index():
    mission = collection.find_one()
    # if 'Table' in mission:
    #     table_dict = mission[0]['Table']
    #     df = pd.DataFrame.from_dict(table_dict)
    #     table_html = df.to_html
    # else:
    #     table_html = None
    return render_template('index.html', mission=mission)

# Create route that will trigger scrape functions
@app.route('/scrape')
def scrape():
    mission = scrape_mars.scrape()
    db.mission.drop()

    # Combine results into one dictionary
    # forecast = {
    #     'location': weather['location'],
    #     'date': weather['date'],
    #     'max_temp': weather['max_temp'],
    #     'min_temp': weather['min_temp'],
    #     'surf_spot': surf['surf_spot'],
    #     'surf_height': surf['surf_height'],
    # }

    # Insert forecast into database
    collection.insert_one(mission)

    # Redirect back to home page
    return redirect('/', code=302)

if __name__ == '__main__':
    app.run(debug=True)