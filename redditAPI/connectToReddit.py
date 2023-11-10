import requests
from redditAPI.redditInfo import CLIENT_ID, SECRET_TOKEN

# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN)

def readPassword():
    with open("redditAPI/pw.txt", "r") as f:
        pw = f.read()
    return pw

def loginToUser():
    # here we pass our login method (password), username, and password
    data = {'grant_type': 'password',
            'username': 'OneVsALL',
            'password': readPassword()}
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