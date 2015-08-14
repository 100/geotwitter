import tweepy
import requests
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
        url = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + self.zipcode
        latN = (float)url.json()['results'][0]['geometry']['bounds']['northeast']['lat']
        longN= (float)url.json()['results'][0]['geometry']['bounds']['northeast']['long']
        latS = (float)url.json()['results'][0]['geometry']['bounds']['southwest']['lat']
        longS= (float)url.json()['results'][0]['geometry']['bounds']['southwest']['long']
        lat = (latN + latS) / 2
        long = (longN + longS) / 2

        earth = 6371000; #meters
        φ1 = radians(latN)
        φ2 = radians(latS)
        Δφ = radians(latN-latS)
        Δλ = radians(longN-longS)
        a = sin(Δφ/2) * sin(Δφ/2) +
                cos(φ1) * cos(φ2) *
                sin(Δλ/2) * sin(Δλ/2)
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        d = fabs(earth * c)  #Haversine formula

        return lat, long, d/2

    
