from googleplaces import GooglePlaces, types, lang
import os,sys
import json

def get_api_key():
	try:
		apikey=os.environ['GOOGLE_PLACES_API_KEY']
		if apikey:
			return apikey
	except:
		print("Terminating - Key not set \n Use export GOOGLE_PLACES_API_KEY=\"key\"")
		sys.exit()	



def get_place(name,location,radius=5,types=[types.TYPE_FOOD]):
	apikey = get_api_key()
	google_places = GooglePlaces(apikey)
	query_result = google_places.nearby_search(name=name,location=location, radius=radius, types=types)
	return query_result.places[0]

def get_place_id(place):
	return place.place_id	
	
def get_place_details(place):
	place.get_details()
	details = place.details
	
	
	mydict={}
	
	mydict['rating']=str(details['rating'])
	mydict['name']=str(details['name'])
	mydict['reviews']=details['reviews']
	mydict['location']=str(details['formatted_address'])

	return mydict

if __name__=='__main__':
	#p = get_place('RockysLounge','40.3964688,-80.0849416')
	#main('ASifDajshf','Arizona Pizza Company','33.65379,-112.23381')
	p = get_place('Fatburger','33.42596,-111.94025')
	#p = get_place('Hummus Xpress','33.4078,-111.95375')
	print get_place_details(p)



