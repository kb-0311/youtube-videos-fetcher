# FamPay Backend Internship Assignment

Used Flask API and MongoDB as the database

## Table of Contents

- [Project Goal](#project-goal)
- [Basic Requirements](#basic-requirements)
- [Features Implemented](#features-implemented)
- [Usage](#usage)

## Project Goal
To make an API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

## Requirements Implemented

The project fulfills the following requirements :

- Continuously (at an interval of 10 seconds) fetch the latest videos from YouTube for a predefined search query (here 'Cricket' is the default).
- Store relevant data of videos (e.g., video title, description, publishing datetime, thumbnails URLs) in a MongoDB database.
- Provide a GET API to retrieve the stored video data in a paginated response sorted in descending order of published datetime.
#### + Bonus requirement implemented
- Added support for supplying multiple API keys so that if quota is exhausted on one, it automatically uses the next available key.Additionally it follows a round scheduling algo where a list of api keys can be used 
for each new request in a circular manner (after last api key is used , the scheduling starts with the first one again)

## Usage

### Prerequisites

Before running the project, ensure you have the following prerequisites:

1. **YouTube API Key:** Obtain an API key from the [Google Developers Console](https://console.developers.google.com/) by creating a new project and enabling the YouTube Data API v3. Ensure the API key has the necessary permissions to access the required YouTube resources.
You can have multiple api keys with env names 'API_KEY_1' , 'API_KEY_2' .... etc and pull and append the env variable to the API_KEYS global list.
2. **MongoDB Instance:** You need to have a MongoDB instance running either locally or on MongoDB Atlas. If running locally, make sure MongoDB is installed and running on your system. If using MongoDB Atlas, sign up for an account and create a cluster. Make note of the connection URI and database credentials.
configure 'MONGODB_URI' env variable accordingly
### Running the Project

Follow these steps to set up and run the project:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/kb-0311/youtube-videos-fetcher/
   cd youtube-videos-fetcher/
   ```
2. **Setup Flask-API**
   ```bash
   . .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Start the application**
   ```bash
   flask --app videoFetching --debug run
   ```

## Endpoints :
1. '/': queries the database for stored video data and returns them in a paginated, sorted order.
2. 'videos/latest': makes a request to the youtube api to fetch latest cricket videos
3. keyScheduling: used for rotation of api keys
4. videoScheduling: makes request to '/videos/latest' at regular intervals

   


