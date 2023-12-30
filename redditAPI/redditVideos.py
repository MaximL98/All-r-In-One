import praw
from redditInf import CLIENT_ID, SECRET_TOKEN

def readPassword():
    with open("redditAPI/pw.txt", "r") as f:
        pw = f.read()
    return pw

def readUsername():
    with open("redditAPI/username.txt", "r") as f:
        username = f.read()
    return username
    
def get_video(post_id):
    # Create a Reddit instance
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=SECRET_TOKEN,
                         username=readUsername(),
                         password=readPassword(),
                         user_agent='MyBot/0.0.1')

    # Access the subreddit and get the submission (post) by ID
    submission = reddit.submission(id=post_id)

    # Extract the video URL from the submission
    video_url = submission.media['reddit_video']['fallback_url']
    print(f"video_url={video_url}")
    return video_url