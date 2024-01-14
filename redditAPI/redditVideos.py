import praw
import os 
from dotenv import dotenv_values

config = dotenv_values("config.env")
CLIENT_ID = config['CLIENT_ID']
SECRET_TOKEN = config['SECRET_TOKEN']
PASSWORD = config["PASSWORD"]
USERNAME = config["USERNAME"]
    
def get_video(post_id):
    # Create a Reddit instance
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=SECRET_TOKEN,
                         username=USERNAME,
                         password=PASSWORD,
                         user_agent='MyBot/0.0.1')

    # Access the subreddit and get the submission (post) by ID
    submission = reddit.submission(id=post_id)
    print(submission.media)
    # Extract the video URL from the submission
    video_url = submission.media['reddit_video']['fallback_url']
    return video_url