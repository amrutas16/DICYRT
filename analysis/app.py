from flask import Flask,redirect, url_for, request
import unicodedata,main
from flask import Markup
from flask import Flask
from flask import render_template
import ast
import json
from setting_logs import set_log
app = Flask(__name__,static_folder ="static")

@app.route("/searchrestaurant")
def searchR():
    return render_template('searchrestaurant.html')

@app.route("/")
def display():
    print 'Home page'
    return render_template('main.html')

'''
@app.route("/restaurant" , methods = [ 'GET'])
def searchrestaurant():
    if request.method == 'GET':
        food = request.args.get('food')
        city=request.args.get('city')
    j={}    
    return render_template('restaurant.html')
'''

@app.route("/maps", methods = ['POST'])
def searchMaps():
    if request.method == 'POST':
        food = request.form.get('food', type=str) 
        city = request.form.get('city', type=str)
    set_log("INFO", "logs", "Search for top restaurants serving " + food + " in " + city)
    #  restaurant_data = {"restaurants":[
    # {"restName":"London Eye, London", "lat": 51.503454, "lng": -0.119562, "address": "Address1", "rating" : 4},
    # {"restName":"Palace of Westminster, London", "lat": 51.499633, "lng": -0.124755, "address": "Address2", "rating" : 5}]};
    restaurant_data = {"restaurants":[
    {"restName":"Senor Taco", "lat": 33.45221, "lng": -112.39201, "address": "525 N Estrella Pkwy Ste 100 Goodyear, AZ 85338", "rating" : 3.5},
    {"restName":"Senor Taco", "lat": 33.46238, "lng": -112.36042, "address": "525 N Estrella Pkwy Ste 100 Goodyear, AZ 85338", "rating" : 3.5},
    {"restName":"Senor Taco", "lat": 33.4627, "lng": -112.34153, "address": "525 N Estrella Pkwy Ste 100 Goodyear, AZ 85338", "rating" : 3.5},
    {"restName":"Senor Taco", "lat": 33.46434, "lng": -112.39023, "address": "525 N Estrella Pkwy Ste 100 Goodyear, AZ 85338", "rating" : 3.5},
    {"restName":"Senor Taco", "lat": 33.46177, "lng": -112.34428, "address": "525 N Estrella Pkwy Ste 100 Goodyear, AZ 85338", "rating" : 3.5},
    {"restName":"Senor Taco", "lat": 33.36024, "lng": -112.4053, "address": "525 N Estrella Pkwy Ste 100 Goodyear, AZ 85338", "rating" : 3.5},
    {"restName":"Senor Taco", "lat": 33.41045, "lng": -112.39265, "address": "525 N Estrella Pkwy Ste 100 Goodyear, AZ 85338", "rating" : 3.5},
    {"restName":"Senor Taco", "lat": 33.46379, "lng": -112.34559, "address": "525 N Estrella Pkwy Ste 100 Goodyear, AZ 85338", "rating" : 3.5},
    {"restName":"Senor Taco", "lat": 33.45223, "lng": -112.39167, "address": "525 N Estrella Pkwy Ste 100 Goodyear, AZ 85338", "rating" : 3.5},
    {"restName":"Palace of Westminster, London", "lat": 33.43654 , "lng": -112.42171, "address": "Address2", "rating" : 5}]};
    data = main.search_query_1(food, city)
    transformed_data = {"restaurants" : [ast.literal_eval(json.dumps(i)) for i in data]}
    #print transformed_data
    #set_log("INFO", "logs", "The top 10 restaurants for " + str(food) + " in " + str(city) + " are: " + str(transformed_data))
    set_log("INFO", "debug", "The top 10 restaurants for " + str(food) + " in " + str(city) + " are: " + str(transformed_data))
    return render_template('map.html', restaurant_data=transformed_data)


@app.route("/searchfood")
def searchF():
    return render_template('searchfood.html')


@app.route("/food",methods = [ 'GET'])
def chart():
    """{'business_id': u'jRPtR43eLXJmnr9Mw_deMg', 'food_list': [(u'sandwich', 15), (u'fish', 3), (u'chicken', 2)]}"""
    #j={'business_id': u'jRPtR43eLXJmnr9Mw_deMg', 'food_list': [(u'sandwich', 15), (u'fish', 3), (u'chicken', 2)]}
    #j=search_query_2(,)

    if request.method == 'GET':
    	restaurant = request.args.get('name')
    	city = request.args.get('city')
    	j = {}
        set_log("INFO", "logs", "Searching for top food items in " + restaurant + " in " + city)
	j = main.search_query_2(restaurant,city)
	if bool(j):
		title = "Food at "+ restaurant
    		labels =  [list([x[0].encode('ascii','ignore'),x[1]]) for x in j['food_list']]
    		print labels
    		return render_template('food.html', title=title,labels=labels)
	#else: return error 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6002,debug=True)
