import tweepy


key_secret = open("../secrets/access_key_secret").readline()[:-1]
key = open("../secrets/access_key").readline()[:-1]

token_secret = open("../secrets/access_token_secret").readline()[:-1]
token = open("../secrets/access_token").readline()[:-1]


auth = tweepy.OAuthHandler(key, key_secret)
auth.set_access_token(token, token_secret)

print((token, token_secret, key, key_secret))
api = tweepy.API(auth)

api.update_status(status = "patience patience patience")
