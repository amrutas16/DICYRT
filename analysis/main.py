import config
import sys
import cass
from google_places_kafka import send_to_kafka
from setting_logs import set_log


def getFoodlist():
    lines=[]
    with open(config.foodlist) as f:
        lines = f.read().splitlines()
    return lines


def search_query_1(food, city):
    food = food.strip()
    city = city.strip()
    #print "The food and city are" + str(food) + " " + str(city)
    #cass.setLog("INFO","Query results 1 for food : "+food+" and city : "+city)
    set_log("INFO", "debug", "Query results 1 for food : "+food+" and city : "+city)
    return cass.get_top_restaurants(food, city)


def search_query_2(restaurant,location):
    cass.setLog("INFO","Query results 2 for restaurant : "+restaurant+" and location : "+location)
    set_log("INFO", "debug", "Query results 2 for restaurant : "+restaurant+" and location : "+location)
    
    b_id = cass.get_business_id(restaurant,location)
    if b_id is None:
        return {}
    else:
        result = cass.get_food_details(b_id)
        msg = "The top foods for restaurant " + str(restaurant) + " are " + repr(result)
        set_log("INFO", "logs", msg)
        #'''
        result_for_kafka = cass.get_business_details_for_kafka(result['business_id'])[0]
        name = result_for_kafka['name']
        lat = result_for_kafka['latitude']
        lng = result_for_kafka['longitude']
        lat_lng = str(lat) + ',' + str(lng)
        send_to_kafka(b_id, name, lat_lng)
        #'''        
        set_log("INFO", "logs", "Making API call for google_places_kafka")
        return result	
        #cass.setLog("INFO", "Making API call for google_places_kafka")


def get_top10_restaurant():
    foodList= getFoodlist()
    print ("FoodList : "+ ','.join(foodList))
    food=raw_input("Enter Food from the list given above : ")
    if (food in foodList):

        location=raw_input("Enter Location where you have to search : ")
        if location is not '':
            search_query_1(food,location)
        else:
            print ("Invalid Location \nERROR: Exiting..")
        sys.exit()
    else:
        print ( "Please Enter from the food list provided \nERROR: Exiting..")
        sys.exit()


def get_top10_food():
    restaurant=raw_input("Enter Restaurant Name : ")
    if (restaurant is not ''):
        location=raw_input("Enter Location where you have to search the restaurant : ")
        if location is not '':
            print search_query_2(restaurant,location)
        else:
            print ("Invalid Location \nERROR: Exiting..")
        sys.exit()
    else:
        print ( "Please Enter restaurant name \nERROR: Exiting..")
        sys.exit()



if __name__=="__main__":
    search_query_1('Tacos', 'Goodyear')
