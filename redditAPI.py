import requests
import pandas as pd
from connectToReddit import headers
import sys
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

def getRequests(headers):
    requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
    res = requests.get("https://oauth.reddit.com/r/aww/hot",
                   headers=headers, params={'limit': '10', 'show': 'true'})
    return res

def getData():
    df = pd.DataFrame()  # initialize dataframe
    for post in getRequests(headers).json()['data']['children']:
        # append relevant data to dataframe
        new_row = pd.DataFrame({
            'subreddit': [post['data']['subreddit']],
            'title': [post['data']['title']],
            'selftext': [post['data']['selftext']],
            'secure_media' : [post['data']['secure_media']],
            'link_url': [post['data']['url']],
            'upvote_ratio': [post['data']['upvote_ratio']],
            'ups': [post['data']['ups']],
            'downs': [post['data']['downs']],
            'score': [post['data']['score']]
            })
        df = pd.concat([df, new_row], ignore_index=True)
    return(df)
        
print(getData())

def writeToTxt(df):
    df.to_string('output.txt')
    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write(df.to_string())
    df.to_csv('output.txt', sep='\t')

writeToTxt(getData())


print(getData()['secure_media'][4]['reddit_video']['fallback_url'])

import cv2

# Create a VideoCapture object
cap = cv2.VideoCapture(getData()['secure_media'][4]['reddit_video']['fallback_url'])

# Check if the video file was opened successfully
if not cap.isOpened():
    print("Error opening video file")

# Read until video is completed
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        # Display the resulting frame
        cv2.imshow('Video', frame)
        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# When everything done, release the video capture and video write objects
cap.release()

# Closes all the frames
cv2.destroyAllWindows()