import praw
import os 
from dotenv import dotenv_values

config = dotenv_values("config.env")
CLIENT_ID = config['CLIENT_ID']
SECRET_TOKEN = config['SECRET_TOKEN']
PASSWORD = config["PASSWORD"]
USERNAME = config["USERNAME"]

def get_gallery(post_id):
    # Create a Reddit instance
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=SECRET_TOKEN,
                         username=USERNAME,
                         password=PASSWORD,
                         user_agent='MyBot/0.0.1')

    # Access the subreddit and get the submission (post) by ID
    submission = reddit.submission(id=post_id)

    list_of_images = []  # Initialize lists
    list_of_images_x = []
    list_of_images_y = []

    for item in sorted(submission.gallery_data['items'], key=lambda x: x['id']):
        media_id = item['media_id']
        meta = submission.media_metadata[media_id]
        if meta['e'] == 'Image':
            source = meta['s']
            list_of_images.append(source['u'])
            list_of_images_x.append(source['x'])
            list_of_images_y.append(source['y'])
            
    return list_of_images, list_of_images_x, list_of_images_y

