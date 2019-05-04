
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream 
import sqlite3
import time
from textblob import TextBlob
from unidecode import unidecode

conn = sqlite3.connect('twitter.db')
c = conn.cursor()

def create_table():
    try:
        c.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)")
        c.execute("CREATE INDEX fast_unix ON sentiment(unix)")
        c.execute("CREATE INDEX fast_tweet ON sentiment(tweet)")
        c.execute("CREATE INDEX fast_sentiment ON sentiment(sentiment)")
        conn.commit()
    except Exception as e:
        print(str(e))
create_table()

#Variables that contains the user credentials to access Twitter API 
access_token = "1090058577606336512-tJlBxmM8OD7Ujwmv0ibgFb3GSUNqD8"
access_token_secret = "UjqYk6spEvWgSc9tVasaGtNawprMy8K74XDWntIs3N1qP"
consumer_key = "szs3099CypNSKmnUXPWd7oK5s"
consumer_secret = "7tWGY0VXWuPrhFJvmaHaKXjpcg6id3dt0ty46tiuW4jp8vkfJF"

date = []
text = []
neg = []
#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):      


    def on_data(self, data):
        try:
            data = json.loads(data)
            tweet = unidecode(data["text"])
            time_ms = data['timestamp_ms']
            sent= TextBlob(tweet)
            print(time_ms,tweet,sent.sentiment.polarity)
            c.execute("INSERT INTO sentiment (unix, tweet, sentiment) VALUES(?,?,?)",(time_ms,tweet,sent.sentiment.polarity))
            conn.commit()
        except KeyError as e:
            print(str(e))
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    while True:
        try:
            l = StdOutListener()
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            #mt.plot()
            stream = Stream(auth, l)

            #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
            stream.filter(languages = ["en"], track=['a','e','i','o','u'])
        except Exception as e:
            print(str(e))
            time.sleep(5)