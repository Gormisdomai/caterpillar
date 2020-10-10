import RPi.GPIO as IO
import time
import subprocess
import tweepy
import logging 
  
log = logging.getLogger(__name__) 

IO.setmode(IO.BCM)


touch_pin = 25
pwm_pin = 17
ain_1_pin = 22
ain_2_pin = 27

slow_speed_frequency = 100
fast_speed_frequency = 300

key_secret = open("../secrets/access_key_secret").readline()[:-1]
key = open("../secrets/access_key").readline()[:-1]

token_secret = open("../secrets/access_token_secret").readline()[:-1]
token = open("../secrets/access_token").readline()[:-1]

last_tweet = open("../data/last_replied_tweet.txt").readline()[:-1]
last_tweet_file = open("../data/last_replied_tweet.txt", "w")

logging.info("setting up twitter API")
auth = tweepy.OAuthHandler(key, key_secret)
auth.set_access_token(token, token_secret)

api = tweepy.API(auth)


def setup():
    logging.info("setting up GPIO")
    slow_speed_frequency = 100
    fast_speed_frequency = 200

    IO.setup(pwm_pin, IO.OUT)
    IO.setup(ain_1_pin, IO.OUT)
    IO.setup(ain_2_pin, IO.OUT)
    IO.setup(touch_pin, IO.IN)


def spin_test():
    pulse = IO.PWM(pwm_pin, fast_speed_frequency)
    IO.output(ain_1_pin, IO.HIGH)
    IO.output(ain_2_pin, IO.LOW)

    pulse.start(50)
    time.sleep(5)
    pulse.stop()


def spin_til_push():
   logging.info("spinning")
   pulse = IO.PWM(pwm_pin, fast_speed_frequency) 
   pulse.start(45)
   logging.info("ignoring touch input for 1.5 seconds")
   time.sleep(1.5)
   logging.info("waiting for touch input")
   while IO.input(touch_pin) == 0:
      time.sleep(0.1) 
      continue
   logging.info("touch detected, stopping")
   pulse.stop()

# see: https://realpython.com/twitter-bot-python-tweepy/
def reply_to_mentions(since_id):
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        logging.info("found tweet to reply to " + tweet.id)
        if tweet.in_reply_to_status_id is not None:
            continue
        roll_die()
        save_since_id(since_id)
        tweet_image(tweet)
    return new_since_id

def reply_to_mentions_loop():
    since_id = int(last_tweet or 0)
    while True:
        since_id = reply_to_mentions(since_id)
        save_since_id(since_id)
        logging.info("sleeping 60 seconds")
        time.sleep(60)

def cleanup():
    IO.cleanup()


def take_photo():
    subprocess.check_call(["fswebcam", "--crop", "352x200,0x88", "--no-banner", "/tmp/test.jpg"])

def display_photo():
    subprocess.check_call(["fbi", "/tmp/test.jpg"])


def focus_helper():
    while 1:
        take_photo()
        display_photo()


def roll_die():
   logging.info("rolling die")
   spin_til_push()
   take_photo()

def save_since_id(id):
   logging.info("saving since id " + tweet.id)
   last_tweet_file.seek(0)
   last_tweet_file.write(id)
   last_tweet_file.truncate()

def tweet_image(tweet):
   logging.info("tweeting image in reply to " + tweet.id)
   api.update_with_media(
       "/tmp/test.jpg",
       "",
       in_reply_to_status_id=tweet.id,
       auto_populate_reply_metadata=True
   )

if __name__ == "__main__":
   try:
      setup()
      reply_to_mentions_loop()
   finally:
      cleanup()


