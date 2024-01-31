from apscheduler.schedulers.background import BackgroundScheduler
import requests
from flask import Flask, abort
from . import API_KEYS


def fetch_latest_videos_periodically():
    # Create a scheduler
    scheduler = BackgroundScheduler()

    
    def call_video_fetcher():
        # number of API KEYs used to fetch videos
        k = 1
        while True:
            # makes an API request to video fetcher
            url = 'http://localhost:5000/videos/latest' 
            response = requests.get(url)
            if response.status_code == 200:
                print("Endpoint called successfully")
                break
            
            # exhausted API KEYs 
            if k==len(API_KEYS):
                abort(500)


            print("Error calling endpoint")
            k+=1

    # Add the cron job to the scheduler
    scheduler.add_job(call_video_fetcher, 'interval', seconds=10)  # Run every 10 seconds

    # Start the scheduler
    scheduler.start()