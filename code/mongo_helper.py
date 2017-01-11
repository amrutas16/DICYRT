from pymongo import MongoClient
from datetime import datetime
import sys

sys.dont_write_bytecode=True

client = MongoClient("mongodb://mongoserver:27017")
db = client.test

def insert(coll,json):
	#result = db.food_restaurant_mapping.insert( {review_id :"5UmKMjU",source:"yelp", restaurant_name:"Mr Hoagie" ,location_city:"Dravosburg" ,food:"Biryani", business_id:"5UmKMjUEUNdYWqANhGckJw"})
	"""
	try:
		mydict={}
		mydict["review_id"]=review_id
		mydict["source"]=source
		mydict["restaurant_name"]=restaurant_name
		mydict["location_city"]=location_city
		mydict["food"]=food
		mydict["business_id"]=business_id
		#print mydict
		result = coll.insert(mydict)
		#print result
	except:
		print ("Fatal Exception while inserting ",review_id,source,restaurant_name,location_city,food,business_id)
	"""
	coll.insert(json)
	
def select(coll):
	global client
	global db
	cursor = coll.find()
	for document in cursor:
    		print(document)
	



if __name__=="__main__":
	#select(db.food_restaurant_mapping)
	#insert(db.business,"5UmKMjU","yelp", "Mr Hoagie" ,"Dravosburg" ,"Biryani","5UmKMjUEUNdYWqANhGckJw")
	select(db.business)





