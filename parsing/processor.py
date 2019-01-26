import pandas as pd
import re

emotions = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'sadness', 'surprise', 'trust']
emotion_df = pd.read_csv('lexicons_compiled.csv')

def emotion_list(emotion):
    return emotion_df[emotion_df['emotion'] == emotion]['word']

emotion_dict = dict(zip(emotions, list(map(emotion_list, emotions))))

def calculate_emotion_score(text, emotion):
    words = re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', text)).lower().split(' ')
    return sum(emotion_dict[emotion].isin(words))
    

tweets = pd.read_csv('../twitter/data/2019-01-23:2019-01-24.csv')

tweets.columns = ['date','text','cityst','country','platform']

for emotion in emotions:
    tweets[emotion] = tweets['text'].apply(lambda text: calculate_emotion_score(text, emotion))

tweets['date'] = pd.to_datetime(tweets['date'])
tweets['minute'] = tweets['date'].apply(lambda date: date.minute)

print(tweets.groupby('minute').agg('sum').to_csv())

#print(tweets.to_csv())

