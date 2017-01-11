from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import re
import json
#import analyse
import config
import cass
from setting_logs import set_log 
sc = None
words = None
businessid_food_count_list = []

def main():
	global sc, words
	conf = SparkConf().setMaster('local[2]').setAppName(config.spark['appname']).set("spark.driver.maxResultSize", "0").set("spark.executor.heartbeatInterval","600")
	sc = SparkContext(conf=conf)
	ssc = StreamingContext(sc, 10)   # Create a streaming context with batch interval of 10 sec

	words = load_wordlist(config.foodlist)
	#stream(ssc, 10)
	stream(ssc)


def process(rd):
    empty = rd.isEmpty()
    if not empty:
        rd = rd.map(convert_json)
        rd = rd.filter(lambda r: int(r['rating']) >= config.threshold)
        rd = rd.map(parse_json)
        businessid_food_count_list.append(rd.flatMap(extract_food_items).map(lambda bid_fooditem: (bid_fooditem,1)).reduceByKey(lambda a,b : a + b).map(create_tuple).collect())


def stream(ssc):
	kafkaStream = KafkaUtils.createDirectStream(ssc,['google_places'],kafkaParams = {"metadata.broker.list": '152.46.16.173:9092', 'auto.offset.reset': 'smallest'})
	objstream = kafkaStream.map(lambda x: x[1])
	objstream.foreachRDD(lambda rdd: process(rdd))

	ssc.start()
	ssc.awaitTermination()
	#ssc.awaitTerminationOrTimeout(duration)
	#ssc.stop(stopGraceFully=True) 	


def extract_food_items(review):
    food_items = []
    for word in words:
        if word.lower() in review['text'].lower():
            business_id = review['business_id']
            food_items.append(business_id + " " + word)
    return food_items


def load_wordlist(filename):
    text = sc.textFile(filename,4)
	#words = text.flatMap(lambda word: word.split("\n"))
    words = text.flatMap(lambda word: word.split("\n")).map(lambda word: word.split(":")[0])
    return words.collect()


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
    cass.insert_food_details(element,"Google")
    set_log("INFO", "debug", "The tuple is " + repr(element))
    return element


def filterSpecChars(inp):
		#Following approach is inspired from a StackOverflow post
    return re.sub('[^A-Za-z0-9\s]', '', inp).lower()

if __name__=="__main__":
    set_log("INFO", "logs", "Started analyse_streaming.py") 
    main()

