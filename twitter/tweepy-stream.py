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


class listener(StreamListener):

    def on_data(self, data):
        tweet = json.loads(data)
        
        print(tweet["user"]["screen_name"])
        print(tweet["text"])
        print("\n")

        if tweet["place"]:
            print("FOUND GEOTAG\n")
            print(tweet["place"])
            print("\n")

        return(True)

    def on_error(self, status):
        print(status)

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["government shutdown"])
