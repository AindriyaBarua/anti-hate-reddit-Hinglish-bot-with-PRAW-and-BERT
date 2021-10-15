import praw
import pickle
from simpletransformers

import constants

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

def detect_warn(subreddit, model):
    # check every comment in the subreddit
    for comment in subreddit.stream.comments():
        if "Anti Hate Bot says:" not in comment.body:
          prediction, raw_output = model.predict([comment.body])
          if prediction == 1:
              comment.reply("Anti Hate Bot says: This is hate speech. Please be respectful here!")


if __name__ == '__main__':
    reddit = get_reddit_instance()
    subreddit = get_subreddit(reddit)
    model = load_hate_detection_model()
    detect_warn(subreddit, model)


