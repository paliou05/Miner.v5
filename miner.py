import tweepy
import time
import pymongo
import os
import json
import networkx as nx
import matplotlib.pyplot as plt
from db_insert import Database_Inserting	

auth = tweepy.OAuthHandler("")
auth.set_access_token("")
api = tweepy.API(auth)

	
def find_timeline(username):
	timeline = api.user_timeline(username)
	return timeline

def get_user_id(username):
	user = api.get_user(screen_name=username)
	user_id = user.id
	return user_id
	
def find_first_tweet(timeline):
	retweet = timeline[0]
	return retweet
		
def get_orig_tw_id(retweet):
	retweet_id = retweet.retweeted_status.id
	return retweet_id
		
def get_orig_tw(retweet_id):
	original_tweet = api.get_status(retweet_id)
	return original_tweet
		
def get_rt_ids(original_tweet):
	retweet_ids = api.retweets(original_tweet.id)
	return retweet_ids
	
def get_followers(retweet_ids):
	for i in retweet_ids:
		#retweeters screen names
		retweeters = i.author.screen_name
		#retweeters ids
		ids = []
		for page in tweepy.Cursor(api.followers_ids, screen_name=retweeters).pages():
			ids.extend(page)
			time.sleep(60)
	return retweeters,ids
		
def get_followers_count(retweeters_ids):
	followers_count = len(retweeters_ids)
	return followers_count
		
	
def get_followers_ids(followers_count,retweeters):
	followers = api.followers(screen_name=retweeters)
	for f in range(len(followers)):
		status = followers[f]
		followers_ids = status.id
	return followers_ids,followers
	
def find_matches(followers,followers_ids,retweet_ids,original_tweet):
	g = nx.Graph()
	for f in followers_ids:
		for r in retweet_ids:
			if followers_ids == r:
				g.add_node(followers.id)
				g.add_node(r)
				g.add_edge(followers.id,r)
				print "its a match!!!!!!!!!!!!!!!!"
			elif followers_ids == original_tweet.author.id:
				g.add_node(r)
				g.add_node(original_tweet.author.id)
				g.add_edge(r,original_tweet.author.id)
				print "its a match!!!!!!!!!!!!!!!!"
			else:
				g.add_node(r)
				g.add_node(original_tweet.author.id)
				g.add_edge(r,original_tweet.author.id)
				print "no match"
	print nx.info(g)
	nx.draw(g)
	plt.show

def main():
	username = input ("Type the user's name")
	timeline= find_timeline(username)
	user_id = get_user_id(username)
	print "stage 1"
	retweet = find_first_tweet(timeline)
	print "stage 2"
	retweet_id = get_orig_tw_id(retweet)
	print "stage 3"
	original_tweet = get_orig_tw(retweet_id)
	print "stage 4"
	retweet_ids = get_rt_ids(original_tweet)
	print "stage 5"
	retweeters_ids = get_followers(retweet_ids)
	print "stage 6"
	retweeters = get_followers(retweet_ids)
	print "stage 7"
	ids = get_followers(retweet_ids)
	print "stage 8"
	followers_count = get_followers_count(retweeters_ids)
	print "stage 9"
	followers_ids = get_followers_ids(followers_count,retweeters)
	print "stage 10"
	followers = get_followers_ids(followers_count,retweeters)
	print "stage 11"
	find_matches(followers,followers_ids,retweet_ids,original_tweet)
	print "stage 12"
	db_insert = Database_Inserting()
	print "User_id" ,user_id
	time.sleep(60)
	print "retweeters", retweeters
	time.sleep(60)
	print "ids", ids
	time.sleep(60)
	print "followers_ids", followers_ids
	time.sleep(60)
	print "retweet_id", retweet_id
	time.sleep(60)
	print "original_tweet_author_id", original_tweet.author.id
	time.sleep(60)
	print "retweet_ids", retweet_ids
	time.sleep(60)
	print "tweet.text", original_tweet.text
	time.sleep(60)
	db_data = {"id":user_id,
		"screen_name":retweeters,
		"followers":ids,
		"followers_ids":followers_ids,
		"tweet_id":retweet_id,
		#"tag":tag,
		"author id":original_tweet.author.id,
		"retweeted id":retweet_ids,
		"tweet text":original_tweet.text,
		#"created date":created_date
		}
	dataJSON = json.dumps(db_data)
	print "done"
	db_insert.insert_to_db(dataJSON)
if __name__ == '__main__':
	main()