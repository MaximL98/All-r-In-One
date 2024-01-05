import requests
import sys
import os 
from dotenv import dotenv_values

config = dotenv_values("config.env")
PATH_TO_REDDIT_API = config["PATH_TO_REDDIT_API"]
CLIENT_ID = config['CLIENT_ID']
SECRET_TOKEN = config['SECRET_TOKEN']
PASSWORD = config["PASSWORD"]
USERNAME = config["USERNAME"]

sys.path.append(PATH_TO_REDDIT_API)

auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN)

def loginToUser():
    # here we pass our login method (password), username, and password
    data = {'grant_type': 'password',
            'username': USERNAME,
            'password': PASSWORD}
    return data

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'MyBot/0.0.1'}

# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=loginToUser(), headers=headers)

# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
HEADERS = {**headers, **{'Authorization': f"bearer {TOKEN}"}}