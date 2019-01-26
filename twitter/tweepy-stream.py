import json

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

# load our API credentials
import sys
sys.path.append(".")
import config

consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_key
access_token_secret = config.access_secret

def process_tweet(tweet):
    platform = ""
    if tweet["source"].find("iphone") != -1:
        platform = "I"
    if tweet["source"].find("android") != -1:
        platform = "A"
    if tweet["source"].find("ipad") != -1:
        platform = "P"
    if tweet["source"].find("web") != -1:
        platform = "W"
    if tweet["source"].find("mac") != -1:
        platform = "M"
    if tweet["source"].find("PC") != -1:
        platform = "C"

    full_name = ""
    country = ""
    if tweet["place"]:
        full_name = tweet["place"]["full_name"]
        country = tweet["place"]["country"]

    return [tweet["created_at"], tweet["text"].encode('utf-8'), full_name, country, platform]


class listener(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data)
        print(process_tweet(tweet))
        return(True)

    def on_error(self, status):
        print(status)

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["government shutdown"])
