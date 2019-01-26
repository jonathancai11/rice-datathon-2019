import json
import csv
import time
from datetime import timedelta, date, datetime

import tweepy
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


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth)


# csv writer
csvFile = open('data/' + 'week-full.csv', 'a')
csvWriter = csv.writer(csvFile)
# write first row
csvWriter.writerow(["time", "text", "full_name", "country", "platform"])


query = "government shutdown"

today = datetime.today().date()
week_ago = today - timedelta(7)

start_date = week_ago

while start_date < today:
    end_date = start_date + timedelta(1)
    c = Cursor(api.search,
                           q=query,
                           since=start_date.strftime('%Y-%m-%d'),
                           until=end_date.strftime('%Y-%m-%d'),
                           lang="en").items(400)
    while True:
        try:
            data = c.next()
            tweet = data._json
            print(tweet["created_at"], tweet["source"])
            csvWriter.writerow(process_tweet(tweet))
        except tweepy.TweepError:
            print("-------------------- GOT ERROR --------------------")
            time.sleep(60)
            continue
        except StopIteration:
            break
    start_date += timedelta(1)


# write to csv
# csvFile = open('data/' + since_date + ':' + until_date + '.csv', 'a')
# csvWriter = csv.writer(csvFile)
# write header row
# csvWriter.writerow(["time", "text", "full_name", "country", "platform"])

# for data in Cursor(api.search,
#                            q=query,
#                            since=since_date,
#                            until=until_date,
#                            lang="en").items():
#     tweet = data._json
#     print(tweet["created_at"], tweet["source"])

#     csvWriter.writerow(process_tweet(tweet))
