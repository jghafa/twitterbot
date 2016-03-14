#!/usr/bin/python3
import tweepy
import os
import datetime
import sqlite3
import configparser

config = configparser.ConfigParser()
config.read('twitter.ini')

# directory of problems to score
senders = config['data']['Senders'].split(',')
EventTag = config['data']['EventTag']

SQLconn = sqlite3.connect('passport.sqlite')
SQL = SQLconn.cursor()
SQL.execute("""
        create table if not exists passport (
            tweet   text,
            sender  text,
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

query = EventTag.upper() + ' OR ' + EventTag.lower()

#for sname in senders:
if 1 == 1:
    #tweets = api.user_timeline(screen_name = sname, count = 10)
    tweets = api.search(q=query, count = 10)
    #print (dir(tweets[0]))

    for chirp in tweets:

        if EventTag.upper() in chirp.text.upper():
            print ('text      = '+chirp.text)
            print ('id        = '+chirp.id_str)
            print ('name      = '+chirp.author._json['screen_name'])
            print ('created_at= '+chirp.created_at.strftime('%y/%m/%d %H:%M:%S'))
            print ()
            SQL.execute("""INSERT or IGNORE into passport 
                            values (?,?,?,?)""", 
                           (chirp.text, 
                            chirp.author._json['screen_name'],
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

print ('Status Search Remaining: ', end='')
#print (status['resources']['statuses']['/statuses/user_timeline'])
print (status['resources']['search']['/search/tweets']['remaining'], ' ', end='')
print (datetime.datetime.fromtimestamp(
        status['resources']['search']['/search/tweets']['reset']
        ).strftime('%Y-%m-%d %H:%M:%S'))

print ('Application Remaining: ', end='')
#print (status['resources']['application']['/application/rate_limit_status'])
print (status['resources']['application']['/application/rate_limit_status']['remaining'],  ' ', end='')
print (datetime.datetime.fromtimestamp(
        status['resources']['application']['/application/rate_limit_status']['reset']
        ).strftime('%Y-%m-%d %H:%M:%S'))
'''
for s in status:
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
