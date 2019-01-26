import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns

from pylab import rcParams
rcParams['figure.figsize'] = 30, 10

emotions = ['fear', 'anger',  'disgust', 'sadness', 'surprise', 'anticipation', 'joy', 'trust']
emotion_colors = ['black', 'red']
emotion_df = pd.read_csv('lexicons_compiled.csv')

def emotion_list(emotion):
    return emotion_df[emotion_df['emotion'] == emotion]['word']

emotion_dict = dict(zip(emotions, list(map(emotion_list, emotions))))

def calculate_emotion_score(text, emotion):
    words = re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', text)).lower().split(' ')
    return sum(emotion_dict[emotion].isin(words))
    

tweets = pd.read_csv('../twitter/data/week-full.csv')

tweets.columns = ['date','text','cityst','country','platform']

for emotion in emotions:
    tweets[emotion] = tweets['text'].apply(lambda text: calculate_emotion_score(text, emotion))

tweets['date'] = pd.to_datetime(tweets['date'])
tweets['minute'] = tweets['date'].apply(lambda date: date.minute)
tweets['second'] = tweets['date'].apply(lambda date: date.second)
tweets['day'] = tweets['date'].apply(lambda date: date.day)

grouper = tweets.groupby('day').agg('sum')
print(grouper.to_json())
grouper = grouper.reset_index()

#print(grouper[emotions].values)

#second_grouper = tweets.groupby('second').agg('sum').reset_index()
#print(second_grouper['second'].values)
#print(second_grouper[emotions].values)

plt.stackplot(grouper['day'].values, grouper[emotions].values.T, labels=emotions)
plt.title("One Week")
plt.legend(loc='best')
plt.show()

