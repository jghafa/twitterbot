#!/usr/bin/python3
import tweepy
import os
#from tweepy import OAuthHandler

consumer_key = os.environ['CKEY']
consumer_secret = os.environ['CSRT']
access_token = os.environ['ATOK']
access_secret = os.environ['ASRT']
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

user = api.me()
 
print('Name: ' + user.name)
print ()

# Get the User object for twitter...
user = api.get_user('jameshaley')
print (user.screen_name)
print (user.followers_count)
for friend in user.friends():
   print (friend.screen_name)
print()

tweets = api.user_timeline(screen_name = 'SpaceX', count = 100)

for chirp in tweets:
    #print (dir(chirp))
    if '@elonmusk' in chirp.text:
        print (chirp.text)
