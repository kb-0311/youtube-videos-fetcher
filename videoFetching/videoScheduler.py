from apscheduler.schedulers.background import BackgroundScheduler
import requests
from flask import Flask, abort
from . import API_KEYS
import time


def fetch_latest_videos_periodically():
    # Create a scheduler
    scheduler = BackgroundScheduler()

    
    def call_video_fetcher():
        # number of API KEYs used to fetch videos
        k = 0
        while True:
            # makes an API request to video fetcher
            url = 'http://localhost:5000/videos/latest' 
            response = requests.get(url)
            k += 1
            print("Attempt:", k)
            print("Response:", response)
            
            if response.status_code == 200:
                print("Endpoint called successfully")
                break
            elif k == len(API_KEYS):
                raise Exception("All API keys exhausted")
            else:
                print("Error calling endpoint")
                time.sleep(1)

    # Add the cron job to the scheduler
    scheduler.add_job(call_video_fetcher, 'interval', seconds=10)  # Run every 10 seconds

    # Start the scheduler
    scheduler.start()