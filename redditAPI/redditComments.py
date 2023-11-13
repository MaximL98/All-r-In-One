import praw
from redditInfo import CLIENT_ID, SECRET_TOKEN

def readPassword():
    with open("redditAPI/pw.txt", "r") as f:
        pw = f.read()
    return pw

def get_comments(subreddit_name, post_id, comment_limit):
    # Create a Reddit instance
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=SECRET_TOKEN,
                         username='OneVsALL',
                         password=readPassword(),
                         user_agent='MyBot/0.0.1')

    # Access the subreddit and get the submission (post) by ID
    subreddit = reddit.subreddit(subreddit_name)
    submission = reddit.submission(id=post_id)

    # Access the comments and print them
    # Filter out MoreComments objects and sort by score
    comments = [comment for comment in submission.comments if isinstance(comment, praw.models.Comment)]
    sorted_comments = sorted(comments, key=lambda comment: comment.score, reverse=True)

    for comment in sorted_comments[:comment_limit]:
        print(comment.body)

subreddit_name = 'worldnews'
post_id = '17tvhqs'
comment_limit = 5

get_comments(subreddit_name, post_id, comment_limit)
