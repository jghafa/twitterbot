#!/usr/bin/python3
import tweepy
import os
import datetime
import sqlite3

SQLconn = sqlite3.connect('passport.sqlite')
SQL = SQLconn.cursor()
SQL.execute("""
        create table if not exists passport (
            tweet   text,
            id      text primary key,
            sent    text);
          """)


consumer_key = os.environ['CKEY']
consumer_secret = os.environ['CSRT']
access_token = os.environ['ATOK']
access_secret = os.environ['ASRT']
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

'''
# Get the User object for twitter...
user = api.get_user('jameshaley')
print (user.screen_name)
print (user.followers_count)
for friend in user.friends():
   print (friend.screen_name)
print()
'''
tweets = api.user_timeline(screen_name = 'SpaceX', count = 10)
#print (dir(tweets[0]))

for chirp in tweets:

    if '@elonmusk' in chirp.text:
        print ('text      = '+chirp.text)
        print ('id        = '+chirp.id_str)
        print ('created_at= '+chirp.created_at.strftime('%y/%m/%d %H:%M:%S'))
        print ()
        SQL.execute("""INSERT or IGNORE into passport 
                        values (?,?,?)""", 
                       (chirp.text, 
                        chirp.id_str,
                        chirp.created_at.strftime('%y/%m/%d %H:%M:%S')))
        SQLconn.commit()


SQLconn.close()

status = api.rate_limit_status()
print ('User Timeline Remaining: ', end='')
#print (status['resources']['statuses']['/statuses/user_timeline'])
print (status['resources']['statuses']['/statuses/user_timeline']['remaining'], ' ', end='')
print (datetime.datetime.fromtimestamp(
        status['resources']['statuses']['/statuses/user_timeline']['reset']
        ).strftime('%Y-%m-%d %H:%M:%S'))
print ('Application Remaining: ', end='')
#print (status['resources']['application']['/application/rate_limit_status'])
print (status['resources']['application']['/application/rate_limit_status']['remaining'],  ' ', end='')
print (datetime.datetime.fromtimestamp(
        status['resources']['application']['/application/rate_limit_status']['reset']
        ).strftime('%Y-%m-%d %H:%M:%S'))
'''for s in status:
    #print(s)
    if s == 'rate_limit_context': continue
    for x in status[s]:
        #print (x,':',status[s][x] )
        print ()
        for y in status[s][x]:
            print (s,':',x,':',y,':')
            print (status[s][x][y])
            print ()
            a = input("")
'''
