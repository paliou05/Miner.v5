import pymongo
import os
import json

class Database_Inserting:
	
	def __init__(self):
		self.db = self.connect_to_db('test')
		
	def connect_to_db(self,db_name):
		client = pymongo.MongoClient()
		return client[db_name]
		
	def insert_to_db(self,JSONdata):
		self.db.mine.insert(JSONdata)
		