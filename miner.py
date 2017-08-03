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
		
def find_first_tweet(timeline):
	retweet = timeline[1]
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
	return followers_ids
	
def find_matches(followers,followers_ids,retweet_ids,original_tweet):
	for f in followers_ids:
		for r in retweet_ids:
			if followers_ids == r:
				g.add_node(followers.id)
				g.add_node(r)
				g.add_edge(followers.id,r)
				print "its a match!!!!!!!!!!!!!!!!"
			elif follower_ids == original_tweet.author.id:
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
	timeline=find_timeline(username)
	retweet = find_first_tweet(timeline)
	retweet_id = get_orig_tw_id(retweet)
	original_tweet = get_orig_tw(retweet_id)
	retweet_ids = get_rt_ids(original_tweet)
	retweeters_ids = get_followers(retweet_ids)
	retweeters = get_followers(retweet_ids)
	ids = get_followers(retweet_ids)
	followers_count = get_followers_count(retweeters_ids)
	followers_ids = get_followers_ids(followers_count)
	find_matches(followers_ids,retweet_ids)
	db_insert = Database_Inserting()
	db_data = {"id":user_id,
		"screen_name":retweeters,
		"followers":followers_,
		"followers_ids":followers_ids,
		"tweet_id":tweet_id,
		"tag":tag,
		"author id":author_id,
		"retweeted id":retweeted_id,
		"tweet text":tweet_text,
		"created date":created_date
		}
	dataJSON = json.dumps(db_data)
	db_insert.insert_to_db(dataJSON)
if __name__ == '__main__':
	main()