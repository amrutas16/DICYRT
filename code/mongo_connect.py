
from pymongo import MongoClient 

client = MongoClient("mongodb://mongoserver:27017")
db = client.test

def get_db():
	return db
