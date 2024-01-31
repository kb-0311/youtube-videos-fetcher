from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import (
    Blueprint, flash, g, jsonify, request,
)
from . import db
from datetime import datetime, timedelta
from . import keyScheduling

latest_videos = Blueprint('videos', __name__, url_prefix='/videos')



@latest_videos.route('/latest', methods=['GET'])
def latest_youtube_videos():
    
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    MAX_RESULTS = 10  # Number of videos to fetch
    
    # To fetch cricket videos if nothing is provided in request
    query = request.args.get('query', default='cricket', type=str)  # Default query
    
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=keyScheduling.get_next_key())
    search_response = youtube.search().list(
        q=query,
        type="video",
        order="date",
        part="snippet",
        maxResults=MAX_RESULTS,
        # fetches new videos at 10 seconds interval(== rate of refetching of videos defined in the background scheduler)
        publishedAfter= (datetime.now()-timedelta(seconds=10)).isoformat() + 'Z'
    ).execute()

    videos = []
    
    # fetch and store only the relevant data in the DB
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append({
                "title": search_result["snippet"]["title"],
                "video_id": search_result["id"]["videoId"],
                "thumbnail_url": search_result["snippet"]["thumbnails"]["default"]["url"],
                "publish_time": search_result["snippet"]["publishTime"],
                "description": search_result["snippet"]["description"] if search_result["snippet"]["description"] else "no description"
            })
            
    
    latest_videos_response = jsonify({"videos": videos})

    db.videos.insert_many(videos)
    
    return latest_videos_response