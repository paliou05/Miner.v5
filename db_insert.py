import pymongo
import os
import json

class Database_Inserting:
	
	def __init__(self):
		self.db = self.connect_to_db('test')
		
	def connect_to_db(self,db_name):
		client = pymongo.MongoClient()
		return client[db_name]
		
	def insert_to_db(self,dbname,user_id,screen_name,followers,followers_ids,tweet_id,tag,author_id,retweeted_id,tweet_text,created_date):
		db.dbname.insert(
		{"id":user_id,
		"screen_name":screen_name,
		"followers":followers,
		"followers_ids":followers_ids,
		"tweet_id":tweet_id,
		"tag":tag,
		"author id":author_id,
		"retweeted id":retweeted_id,
		"tweet text":tweet_text,
		"created date":created_date
		}
		)
		