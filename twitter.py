import tweepy
import requests
import itertools
from math import radians, sin, cos, atan2, sqrt, fabs
from private import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class Search:
    def __init__(self, zipcode, query):
        self.zipcode = zipcode
        self.search = query

    def findCoordinatesRadius(self):
        url = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + self.zipcode)
        latN = url.json()['results'][0]['geometry']['bounds']['northeast']['lat']
        longN = url.json()['results'][0]['geometry']['bounds']['northeast']['long']
        latS = url.json()['results'][0]['geometry']['bounds']['southwest']['lat']
        longS = url.json()['results'][0]['geometry']['bounds']['southwest']['long']
        lat = (latN + latS) / 2
        long = (longN + longS) / 2

        earth = 6371000; #meters
        alpha  = radians(latN)
        beta = radians(latS)
        theta = radians(latN-latS)
        phi = radians(longN-longS)
        a = sin(theta/2) * sin(theta/2) + cos(alpha) * cos(beta) * sin(phi/2) * sin(phi/2)
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = fabs(earth * c)/1000 #Haversine formula

        return lat, long, d/2 #approximation of a circle's radius contained within the curved sheet that haversine's formula assumes

    def populateTweets(self):
        lat, long, radius = findCoordinatesRadius(self)
        geo = str(lat) + "," + str(long) + "," + str(radius) + "km"
        tweets = api.search(q=self.search, lang='en', geocode=geo, rpp=100, page=1)

        showcase = tweets[0:5]
        self.showcase = []
        for tweet in showcase:
            self.showcase.append([tweet.text, tweet.user.screen_name])

        hashtagsRaw = [tweet.entities['hashtags'] for tweet in tweets]
        hashtags = list(chain.from_iterable(hashtagsRaw))
        frequency = {}
        for hashtag in hashtags:
            frequency[hashtag] = hashtags.count(hashtag)

        texts = [tweet.text for tweet in tweets]
        self.sentiment = 0.0
        for text in texts:
            param = {'apikey':alchemy_key, 'text':text, 'outputmode':'json'}
            sentiment = requests.get("http://access.alchemyapi.com/calls/text/TextGetTextSentiment", params=param)
            numeric = (float)(sentiment.json()['docSentiment']['score'])
            self.sentiment = self.sentiment + (numeric / len(texts)) #computes average sentiment
