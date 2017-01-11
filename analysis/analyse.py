from pyspark import SparkConf, SparkContext
import re
import json
import sys
#sys.path.append("/home/adhuri/DICYRT/analysis")
import config
import cass
#import setting_logs
from setting_logs import set_log
import socket

sc = None
words = None


def extract_food_items(review):
    food_items = []
    for word in words:
        if word in review['text']:
            business_id = review['business_id']
            food_items.append(business_id + " " + word)
    return food_items


def load_wordlist(filename):
    text = sc.textFile(filename,4)
    #words = text.flatMap(lambda word: word.split("\n"))
    words = text.flatMap(lambda word: word.split("\n")).map(lambda word: word.split(":")[0])
    return words.collect()


def load_reviews(filename):
    text = sc.textFile(filename,4)
    return text

def convert_json(review):
    review = json.loads(review)
    return review

def parse_json(review):
    #review = json.loads(review)
    return {'business_id': review['business_id'], 'text': review['text']}


# returns a tuple (business id, food item, count)
def create_tuple(data):
    arr = data[0].split(" ");
    element = {'business_id': arr[0], 'food': arr[1], 'count': data[1]}
    set_log("INFO", "debug", "The tuple generate on  " +str(socket.gethostname()) + "is "+ str(element))
    cass.insert_food_details(element,"Yelp")
    return element


def main():
    global sc, words
    conf = SparkConf().setMaster(config.spark['server']).setAppName(config.spark['appname']).set("spark.driver.maxResultSize", "0").set("spark.executor.heartbeatInterval","600")
    #conf = SparkConf().setMaster('local[2]').setAppName(config.spark['appname']).set("spark.driver.maxResultSize", "0").set("spark.executor.heartbeatInterval","600")
    sc = SparkContext(conf=conf, pyFiles=['config.py','cass.py','setting_logs.py'])
    set_log("INFO", "logs", "Analysis.py Using Food Dictionary from  " + str(config.foodlist))
    words = load_wordlist(config.foodlist)
 
    set_log("INFO", "logs", "Analysis.py Using Reviews from  " + str(config.reviewlist))
    reviews = load_reviews(config.reviewlist)
    reviews = reviews.map(convert_json)
    set_log("INFO", "logs", "Analysis.py doing analysis on stars threshold  " + str(config.threshold))
    reviews = reviews.filter(lambda r: float(r['stars']) >= config.threshold)
    reviews = reviews.map(parse_json)
    reviews.cache()
    businessid_food_count_list = reviews.flatMap(extract_food_items).map(lambda bid_fooditem: (bid_fooditem,1)).reduceByKey(lambda a,b : a + b)\
                                 .map(create_tuple).collect()
    set_log("INFO", "logs", "Analysis.py completed")


def filterSpecChars(inp):
        #Following approach is inspired from a StackOverflow post
	return re.sub('[^A-Za-z0-9\s]', '', inp).lower()

main()
