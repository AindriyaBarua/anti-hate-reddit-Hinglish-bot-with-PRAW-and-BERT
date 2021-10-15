import praw
import pickle
import simpletransformers

# initialize with appropriate values
client_id = ""
client_secret = ""
username = ""
password = ""
user_agent = "AntiHateIndia by u/huemewpew"

# creating an authorized reddit instance
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     username=username,
                     password=password,
                     user_agent=user_agent)

# the subreddit where the bot is to be live on
target_sub = "indianhatespeechtest"
subreddit = reddit.subreddit(target_sub)


# enchant dictionary
filename = 'model.pkl'
model = pickle.load(open(filename, 'rb'))

# check every comment in the subreddit
for comment in subreddit.stream.comments():
    #comment.reply("Ye bot comment hai")
    if "Anti Hate Bot says:" not in comment.body:
      prediction, raw_output = model.predict([comment.body])
      if(prediction == 1):
          comment.reply("Anti Hate Bot says: This is hate speech. Please be respectful here!")
