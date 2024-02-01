import os

from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.json_util import loads,dumps
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

# connect to a mongodb instance in local machine(for the purposes of this assignment)
client = MongoClient(os.getenv('MONGODB_URI'))
# name of the database
db = client['youtube']

# support for multiple API key, follows round scheduling algorithm
# can contain more than 2 api keys
API_KEYS = [os.getenv('API_KEY_1') , os.getenv('API_KEY_2') ,  os.getenv('API_KEY_3')]
current_key_index = 0


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    
    CORS(app)
    
    from . import videosFetcher
    app.register_blueprint(videosFetcher.latest_videos)
    
    # fetches new videos every 10 seconds
    from . import videoScheduler
    videoScheduler.fetch_latest_videos_periodically()

    
    @app.route('/' , methods=['GET' , 'POST'] )
    def get_videos_paginated():
        
        request_data=request.get_json()
        
        query =request_data.get('query' , dict({}))
        
        
        # Assuming 'page' is the query parameter for the page number
        page = int( request_data.get('page')  if request_data.get('page') is not None else 1)  # Default page is 1 if not provided

        # Define number of items per page and how many entries to skip to get a given page
        per_page = 10 
        skip = (page - 1) * per_page
        
        # sort = on descending order of publishing time
        # skip = skip all the entries in the db before the current page
        # limit = number of entries you want to fetch at a time
        latest_videos= list(db['videos'].find(query).sort('publish_time' , -1).skip(skip).limit(per_page))

        for video in latest_videos:
            video['_id'] = str(video['_id'])
        
        
        number_of_entries = db['videos'].count_documents({})
        
            
        return jsonify({"videos":loads(dumps(latest_videos)) , "docs":number_of_entries })
 
    return app

