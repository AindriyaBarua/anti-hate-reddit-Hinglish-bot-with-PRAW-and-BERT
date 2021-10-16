"""
Developed by Aindriya Barua in October, 2021
"""

import praw
import pickle
from simpletransformers

import constants

hate_comments_count = {}


def get_reddit_instance():
    # creating an authorized reddit instance
    reddit = praw.Reddit(client_id=constants.CLIENT_ID,
                         client_secret=constants.CLIENT_SECRET,
                         username=constants.USERNAME,
                         password=constants.PASSWORD,
                         user_agent=constants.USER_AGENT)
    return reddit


def get_subreddit(reddit):
    # the subreddit where the bot is to be live on
    target_sub = constants.TARGET_SUB
    subreddit = reddit.subreddit(target_sub)
    return subreddit


def load_hate_detection_model():
    model = pickle.load(open(constants.HATE_DETECTION_MODEL, 'rb'))
    return model


def handle_hate(subreddit, comment):
    author = comment.author
    if author not in hate_comments_count:
        hate_comments_count[author] = 1
    else:
        hate_comments_count[author] =  hate_comments_count[author] + 1
    if hate_comments_count[author] <= 3:
        comment.reply(constants.WARNING)
    else:
        subreddit.banned.add(author, ban_reason=constants.BAN_REASON, ban_message=constants.BAN_MESSAGE)
        del hate_comments_count[author]


def detect_hate(subreddit, model):
    # check every comment in the subreddit
    for comment in subreddit.stream.comments():
        if constants.WARNING != comment.body: # skip comments by bot
          prediction, _ = model.predict([comment.body])
          if prediction == 1:
              handle_hate(subreddit, comment)


if __name__ == '__main__':
    reddit = get_reddit_instance()
    subreddit = get_subreddit(reddit)
    model = load_hate_detection_model()
    detect_hate(subreddit, model)
