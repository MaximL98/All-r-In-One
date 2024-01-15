import praw
import pandas as pd
import os 
from dotenv import dotenv_values

config = dotenv_values("config.env")
CLIENT_ID = config['CLIENT_ID']
SECRET_TOKEN = config['SECRET_TOKEN']
PASSWORD = config["PASSWORD"]
USERNAME = config["USERNAME"]


def get_comments(post_id, comment_limit):
    # Create a Reddit instance
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=SECRET_TOKEN,
                         username=USERNAME,
                         password=PASSWORD,
                         user_agent='MyBot/0.0.1')

    # Access the subreddit and get the submission (post) by ID
    submission = reddit.submission(id=post_id)

    # Access the comments and print them
    # Filter out MoreComments objects and sort by score
    comments = [comment for comment in submission.comments if isinstance(comment, praw.models.Comment)]
    sorted_comments = sorted(comments, key=lambda comment: comment.score, reverse=True)

    df = []  # Initialize dataframe

    for comment in sorted_comments[:comment_limit]:
        df.append(comment.body)
    return df