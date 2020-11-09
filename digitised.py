import time
import subprocess
import tweepy
import logging
import os, random
from datetime import datetime
  
log = logging.getLogger(__name__)
log.level = logging.INFO

key_secret = open("../secrets/access_key_secret").readline()[:-1]
key = open("../secrets/access_key").readline()[:-1]

token_secret = open("../secrets/access_token_secret").readline()[:-1]
token = open("../secrets/access_token").readline()[:-1]

last_tweet = open("../data/last_replied_tweet.txt").readline()[:-1]
print("read last_tweet_id " + str(last_tweet))
last_tweet_file = open("../data/last_replied_tweet.txt", "w")

all_replied_tweets = [s[:-1] for s in open("../data/all_replied_tweets.txt").readlines()]
all_replied_tweets_file = open("../data/all_replied_tweets.txt", "a")

time_turned_on = datetime.utcnow()
print("turned on at " + str(time_turned_on))

print("setting up twitter API")
auth = tweepy.OAuthHandler(key, key_secret)
auth.set_access_token(token, token_secret)

api = tweepy.API(auth)

# see: https://realpython.com/twitter-bot-python-tweepy/
def reply_to_mentions(since_id):
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        print("found tweet to reply to " + str(tweet.id))
        if tweet.in_reply_to_status_id is not None:
            print("tweet is a reply, skipping")
            continue
        if tweet.id in all_replied_tweets:
            print("tweet already replied to, skipping")
            continue
        if tweet.created_at < time_turned_on:
            print("tweet is old, skipping... created at: " + str(tweet.created_at) + "turned on: " + str(time_turned_on))
            continue
        save_since_id(since_id)
        tweet_random_image(tweet)
    return new_since_id

def reply_to_mentions_loop():
    since_id = int(last_tweet or 1)
    print("using since_id " + str(since_id))
    while True:
        since_id = reply_to_mentions(since_id)
        save_since_id(since_id)
        print("sleeping 60 seconds")
        time.sleep(60)

def save_since_id(id):
   print("saving since id " + str(id))
   last_tweet_file.seek(0)
   last_tweet_file.write(str(id))
   last_tweet_file.truncate()
   all_replied_tweets_file.write(str(id) + "\n")

def tweet_random_image(tweet):
   print("tweeting random image in reply to " + str(tweet.id))
   try:
      api.update_with_media(
         "/media/usb/images/" + random.choice(os.listdir("/media/usb/images/")),
         tweet.text.replace("@Ask_Caterpillar", ""),
         in_reply_to_status_id=tweet.id,
         auto_populate_reply_metadata=True
      )
   except TweepError as e:
      print("Tweep Error Encountered " + str(e))
    

if __name__ == "__main__":
   reply_to_mentions_loop()
