import json
import csv

from tweepy import Cursor
from tweepy import OAuthHandler
from tweepy import API

# load our API credentials
import sys
sys.path.append(".")
import config

consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_key
access_token_secret = config.access_secret


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)

# write to csv
csvFile = open('data/tweets.csv', 'a')
csvWriter = csv.writer(csvFile)

for data in Cursor(api.search,
                           q="test",
                           since="2019-01-23",
                           until="2019-01-24",
                           lang="en").items():
    tweet = data._json
    print(tweet["created_at"], tweet["text"])
    csvWriter.writerow([tweet["created_at"], tweet["text"].encode('utf-8')])
