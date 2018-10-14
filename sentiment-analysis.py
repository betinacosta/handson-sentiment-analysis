import tweepy
import numpy as np
from textblob import TextBlob

consumer_key='qYiI7jKwy83igXiaeM4ej08Oa'
consumer_secret='ucpme5gY9fkMprOc2Bn7P32WbF8Qw2HUg1YDzTTxQUTRNhn0EV'

access_token='66053667-f7HcYwX57Rz4bS2OdIuD6ASVnynv09nxT0jUuenWd'
access_token_secret='QQ82saBSFdvhVccjqAfgwG7JXwpMHsmkEqEQFUpQOpOgH'

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)
tweets = api.search('Python -filter:retweets')

def is_english(text):
    if text.detect_language() == 'en':
        return True
    return False

def tweet_analysis():
    polarities = []

    for tweet in tweets:
        phrase = TextBlob(tweet.text)

        if not is_english(phrase):
            phrase = TextBlob(str(phrase.translate(to='en')))

        if (phrase.sentiment.polarity != 0.0 and phrase.sentiment.subjectivity != 0.0):
            polarities.append(phrase.sentiment.polarity)

    return polarities

def sentiment_analysis():
    polarity_mean = np.mean(tweet_analysis())

    print('Média: ' + str(polarity_mean))
    if(polarity_mean > 0.0):
        print('POSITIVE')
    else:
        print('NEGATIVE')

sentiment_analysis()

    