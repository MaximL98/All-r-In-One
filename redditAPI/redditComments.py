import praw
from redditInfo import CLIENT_ID, SECRET_TOKEN
import pandas as pd


def readPassword():
    with open("redditAPI/pw.txt", "r") as f:
        pw = f.read()
    return pw

def get_comments(post_id, comment_limit):
    # Create a Reddit instance
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=SECRET_TOKEN,
                         username='OneVsALL',
                         password=readPassword(),
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

'''post_id = '17uz6xa'
comment_limit = 10

#get_comments(subreddit_name, post_id, comment_limit)

def writeToTxt(comments, file_path='redditAPI/comments.txt'):
    with open(file_path, 'w', encoding='utf-8') as f:
        for i, comment in enumerate(comments):
            f.write(f"{i+1}. {comment}\n")
            f.write('\n')  # Add a newline between comments

writeToTxt(get_comments(post_id, comment_limit))'''