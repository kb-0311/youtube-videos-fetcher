from apscheduler.schedulers.background import BackgroundScheduler
import requests


def fetch_latest_videos_periodically():
    # Create a scheduler
    scheduler = BackgroundScheduler()

    
    def call_video_fetcher():
        # makes an API request to video fetcher
        url = 'http://localhost:5000/videos/latest' 
        response = requests.get(url)
        if response.status_code == 200:
            print("Endpoint called successfully")
        else:
            print("Error calling endpoint")

    # Add the cron job to the scheduler
    scheduler.add_job(call_video_fetcher, 'interval', seconds=10)  # Run every 10 seconds

    # Start the scheduler
    scheduler.start()