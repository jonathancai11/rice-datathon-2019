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

since_date = "2019-01-23"
until_date = "2019-01-24"
query = "government shutdown"

# write to csv
csvFile = open('data/' + since_date + ':' + until_date + '.csv', 'a')
csvWriter = csv.writer(csvFile)

for data in Cursor(api.search,
                           q=query,
                           since=since_date,
                           until=until_date,
                           lang="en").items():
    tweet = data._json
    print(tweet["created_at"], tweet["source"])

    platform = ""
    if tweet["source"].find("iPhone") != -1:
        platform = "I"
    if tweet["source"].find("Android") != -1:
        platform = "A"
    if tweet["source"].find("Mac") != -1:
        platform = "M"
    if tweet["source"].find("PC") != -1:
        platform = "P"

    full_name = ""
    country = ""
    if tweet["place"]:
        full_name = tweet["place"]["full_name"]
        country = tweet["place"]["country"]

    csvWriter.writerow([tweet["created_at"], tweet["text"].encode('utf-8'), full_name, country, platform])
