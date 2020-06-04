import tweepy
import time
import pymongo
import os,sys
import json
import networkx as nx
import datetime
from scipy import sparse
import matplotlib.pyplot as plt
from db_insert import Database_Inserting	
#keys and rate limiter for the API


auth = tweepy.OAuthHandler("rGu6mn0bTUHM7jPQDChHixMFC", "yf0oHtfzJTIQcbWu6RilGj8Pfp6UtfvZOGqtqfLE6jYxlpdwwX")
auth.set_access_token("467783707-gmwKzVjGpfRxq09UgGBpmvC8uwnx1ivZu4ARerKR", "W9Fh3UgNficFuOPvNoSqSJ3QC1iJ0M6gQniCvurLxgz7F")
api = tweepy.API(auth, retry_count=3,retry_delay=5, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)


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

#checking the friendship between two given users
def isFollower(author_username,retweeters):
	while True:
		try:
			showfriendship = api.show_friendship(source_screen_name=author_username,target_screen_name=retweeters)
		except tweepy.TweepError as e:
			print e.reason
			time.sleep(60)
			continue
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
    if nx.number_of_nodes(g)>0:
        a = nx.adjacency_matrix(g)
        print(a.todense())
        nx.draw_networkx(g,with_labels=True)
        plt.draw()
        #plt.show()
    else:
        pass
    return (nx.nodes(g),nx.edges(g))

def main():
	#hashtag = input("Type Hashtag")
	#for tweet in tweepy.Cursor(api.search,q=hashtag,count=100).items():
	#	try:
	#		retweet = retweet.retweeted_status.id
	#		retweet_id = get_orig_tw_id(retweet)
	#		print "RETWEET ID"
	#	except:
	#		retweet_id = tweet.id
	#		print retweet_id
	#		print "retweet_id"
		
		#username = input ("Type the user's name")
		#timeline= find_timeline(username)
		#user_id = get_user_id(username)
	print "stage 1-user_id"
		#retweet = find_first_tweet(timeline)
		#print "stage 2-retweet" """
	path = r'C:\Users\paliou05\Desktop\data01\non-rumours'
	files = os.listdir(path)
	for name in files:
		print name
		retweet_id = name
		print "stage 3-retweet_id"
		try:
			original_tweet = get_orig_tw(retweet_id)
		except tweepy.TweepError as e:
			print e.args[0][0]['message']
			continue
		text = (original_tweet.text).encode("utf-8")
		print "stage 4-original tweet & text"
		retweet_ids = get_rt_ids(original_tweet)
		retweeters_ids = get_retweeters_ids(retweet_ids)
		print "stage 5-retweet_ids"
		a = datetime.datetime.now()
		retweeters = get_followers(retweet_ids)
		#print type(retweeters)
		b = datetime.datetime.now()
		c = b-a
		print c
		print "stage 6-retweeters/Rtwtrs followers"
		author_username = get_author_screen_name(original_tweet)
		author_id = get_author_id(original_tweet)
		print "stage 7-author username-id"
		#author_followers = get_author_followers(author_username)
		print "stage 8-author followers"
		#followers_count = get_followers_count(retweet_ids)
		#print followers_count, "!!!!!!!!!!"
		print "stage 9-followers count"
		#find_matches(author_username,retweeters)
		tpl = find_matches(author_username,retweeters)
		(NodeView,EdgeView) = tpl
		print NodeView
		print EdgeView
		#node = json.dumps(NodeView.__dict__)
		#edge = json.dumps(EdgeView.__dict__)
		#print type(EdgeView)
		#print type(edge)
		#print type(node)
		#print edge
		#print node
		print "stage 10-starting MongoDB stage"
		if len(retweeters) == 0 :
			pass
		else:
			db_insert = Database_Inserting()
			db_data = {"tweet_id":retweet_id,
				"author_id":author_id,
				"author_screen_name":author_username,
				#"author_followers":author_followers,
				"retweeters":retweeters,
				"retweeters_ids":retweeters_ids,
				"tweet_text":original_tweet.text,
				"nodes":list(NodeView),
				"edges":list(EdgeView)
				}
			print db_data
			dataJSON = json.dumps(db_data)
			dataJSON = json.loads(dataJSON)
			print "done"
			db_insert.insert_to_db(dataJSON)
		print "ALL DONE"
if __name__ == '__main__':
	main()
