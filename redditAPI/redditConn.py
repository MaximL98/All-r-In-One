import requests
import pandas as pd
import cv2
import sys
import os 
from dotenv import dotenv_values
from connectToReddit import HEADERS

config = dotenv_values("config.env")
PATH_TO_REDDIT_API = config['PATH_TO_REDDIT_API']
sys.path.append(PATH_TO_REDDIT_API)

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

# Function to get requests from reddit API
def getRequests(HEADERS, subreddit):
    requests.get('https://oauth.reddit.com/api/v1/me', headers=HEADERS)
    res = requests.get(f"https://oauth.reddit.com/r/{subreddit}/hot",
                   headers=HEADERS, params={'limit': '10', 'show': 'true'})
    return res

# Function to get the data from the request into a data frame
def getData(subreddit):
    df = pd.DataFrame()  # Initialize dataframe
    for post in getRequests(HEADERS, subreddit).json()['data']['children']:
        # Append relevant data to dataframe
        new_row = pd.DataFrame({
        'subreddit': [post['data']['subreddit']],
        'title': [post['data']['title']],
        'selftext': [post['data']['selftext']],
        'secure_media' : [post['data']['secure_media']],
        'link_url': [post['data']['url']],
        'name': [post['data']['name']],
        'url':[post['data']['url']],
        })
        df = pd.concat([df, new_row], ignore_index=True)
    return(df)