from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

# load our API credentials
import sys
sys.path.append(".")
import config

#consumer key, consumer secret, access token, access secret.
ckey = config.consumer_key
csecret = config.consumer_secret
atoken = config.access_key
asecret = config.access_secret

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

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["government shutdown"])
