import tweepy
import time
import pymongo
import os
import json
import networkx as nx
import datetime
#import matplotlib.pyplot as plt
from db_insert import Database_Inserting	
#keys and rate limiter for the API
auth = tweepy.OAuthHandler("")
auth.set_access_token("")
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)


#getting user's timeline	
def find_timeline(username):
	timeline = api.user_timeline(username)
	return timeline


#getting user's id
def get_user_id(username):
	user = api.get_user(screen_name=username)
	user_id = user.id
	return user_id


#getting the first retweet he made	
def find_first_tweet(timeline):
	retweet = timeline[2]
	return retweet


#getting the original tweet id		
def get_orig_tw_id(retweet):
	retweet_id = retweet.retweeted_status.id
	return retweet_id


#getting the original tweet		
def get_orig_tw(retweet_id):
	original_tweet = api.get_status(retweet_id)
	return original_tweet


#getting the users ids retweeted the tweet		
def get_rt_ids(original_tweet):
	retweet_ids = api.retweets(original_tweet.id, 100)
	return retweet_ids


#makes a list of retweeters screen names
def get_followers(retweet_ids):
	retweeters = []
	for i in retweet_ids:
		retweeters.append(i.author.screen_name)
	return retweeters

#makes a list of retweeters ids
def get_retweeters_ids(retweet_ids):
	retweeters_ids = []
	for i in retweet_ids:
		retweeters_ids.append(i.author.id)
	return retweeters_ids
		
#checking for follower's ids
"""
def get_followers_ids(retweeters):
	flwrs_ids = []
	for i in retweeters:
		ids = []
		for page in tweepy.Cursor(api.followers_ids, screen_name=retweeters).pages():
			ids.extend(page)
		flwrs_ids.append(ids)
	return flwrs_ids
"""


#getting the author screen name
def get_author_screen_name(original_tweet):
	author_username = (original_tweet.author.screen_name).encode("utf-8")
	return author_username


#getting the author id
def get_author_id(original_tweet):
	author_id = original_tweet.author.id
	return author_id


#making a list of the author followers
def get_author_followers(author_username):
	author_followers = []
	for page in tweepy.Cursor(api.followers_ids,screen_name=author_username).pages():
		author_followers.extend(page)
	return author_followers


#getting the count of followers		
def get_followers_count(retweet_ids):
	followers_count = len(retweet_ids)
	return followers_count
		
#followers ids	
"""def get_followers_ids(followers_count,retweeters):
	followers = api.followers(screen_name=retweeters)
	for f in range(len(followers)):
		status = followers[f]
		followers_ids = status.id
	return followers_ids,followers"""

	
#def find_matches(retweeters,flwrs_ids,followers_count,retweet_ids,original_tweet,retweeters_ids,author_followers):


#checking the friendship between two given users
def isFollower(author_username,retweeters):	
	showfriendship = api.show_friendship(source_screen_name=author_username,
                             target_screen_name=retweeters)
	return showfriendship[0].followed_by

#finds matches between users and makes a graph
def find_matches(author_username,retweeters):
	g = nx.Graph()
	unconn = []
	for i in retweeters:
		if isFollower(author_username,i):
			print("%s <=== %s" % (author_username, i))
			g.add_node(i)
			g.add_node(author_username)
			g.add_edge(i,author_username)
		else:
			unconn.append(i)
			
	for i in unconn:
		for j in unconn:
			if isFollower(i,j):
				print("%s <=== %s" % (i, j))
				g.add_node(i)
				g.add_node(j)
				g.add_edge(i,j)
	print nx.info(g)


def main():
	username = input ("Type the user's name")
	timeline= find_timeline(username)
	user_id = get_user_id(username)
	print "stage 1-user_id"
	retweet = find_first_tweet(timeline)
	print "stage 2-retweet"
	retweet_id = get_orig_tw_id(retweet)
	print "stage 3-retweet_id"
	original_tweet = get_orig_tw(retweet_id)
	text = (original_tweet.text).encode("utf-8")
	print "stage 4-original tweet & text"
	retweet_ids = get_rt_ids(original_tweet)
	retweeters_ids = get_retweeters_ids(retweet_ids)
	print "stage 5-retweet_ids"
	a = datetime.datetime.now()
	retweeters = get_followers(retweet_ids)
	b = datetime.datetime.now()
	c = b-a
	print c
	print "stage 6-retweeters/Rtwtrs followers"
	author_username = get_author_screen_name(original_tweet)
	author_id = get_author_id(original_tweet)
	print "stage 7-author username-id"
	author_followers = get_author_followers(author_username)
	print "stage 8-author followers"
	followers_count = get_followers_count(retweet_ids)
	print "stage 9-followers count"
	find_matches(author_username,retweeters)
	print "stage 10-starting MongoDB stage"
	db_insert = Database_Inserting()
	db_data = {"author_id":author_id,
		"author_screen_name":author_username,
		"author_followers":author_followers,
		"retweeters":retweeters,
		"tweet_text":original_tweet.text,
		}
	dataJSON = json.dumps(db_data)
	dataJSON = json.loads(dataJSON)
	print "done"
	db_insert.insert_to_db(dataJSON)
	print "ALL DONE"
if __name__ == '__main__':
	main()
