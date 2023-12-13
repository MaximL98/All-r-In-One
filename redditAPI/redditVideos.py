import praw
from redditInfo import CLIENT_ID, SECRET_TOKEN

def readPassword():
    with open("redditAPI/pw.txt", "r") as f:
        pw = f.read()
    return pw

def get_video(post_id):
    # Create a Reddit instance
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=SECRET_TOKEN,
                         username='OneVsALL',
                         password=readPassword(),
                         user_agent='MyBot/0.0.1')

    # Access the subreddit and get the submission (post) by ID
    submission = reddit.submission(id=post_id)

    # Extract the video URL from the submission
    video_url = submission.media['reddit_video']['fallback_url']
    print(f"video_url={video_url}")
    return video_url