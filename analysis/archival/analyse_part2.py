from pyspark import SparkConf, SparkContext
import re
import json
import config
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

ssc =None
sc = None
words = None

def main():
    global sc, words,ssc
    conf = SparkConf().setMaster(config.spark['server']).setAppName(config.spark['appname']).set("spark.driver.maxResultSize", "0").set("spark.executor.heartbeatInterval","3600")
    sc = SparkContext(conf=conf)
    ssc = StreamingContext(sc, 10)   # Create a streaming context with batch interval of 10 sec
    #ssc.checkpoint("checkpoint")

    words = load_wordlist(config.foodlist)
    reviews = load_reviews(config.reviewlist)

    #import code;code.interact(local=locals())
    #sentiment = stream(ssc, words, reviews)
    stream(ssc, words, reviews)
    #sentiment.pprint()


def load_wordlist(filename):
    """
    This function should return a list or set of words from the given filename.
    """
    # YOUR CODE HERE
    text = sc.textFile(filename,4)
    words = text.flatMap(lambda word: word.split("\n"))
    return words.collect()

def load_reviews(filename):
    """
    This function should return a list or set of words from the given filename.
    """
    # YOUR CODE HERE
    text = sc.textFile(filename,4)
    #print text.collect()[0]
    words = text.flatMap(lambda word: word.split("\n"))
    return words.collect()

def filterSpecChars(inp):
	#Following approach is inspired from a StackOverflow post
	return re.sub('[^A-Za-z0-9\s]', '', inp).lower()

def checkWord(word):
    if(word in words):
    	return (word, 1)
    else:
    	return ("none", 1)

def uniqueWords(review):
    return ' '.join(list(set(review.split(" "))))

def updateFunction(newValues, runningCount):
    if runningCount is None:
       runningCount = 0
    return sum(newValues, runningCount)

def stream(ssc,words, reviews):

    kstream = KafkaUtils.createDirectStream(
        ssc, topics = ['google_places'], kafkaParams = {"metadata.broker.list": '152.46.16.173:9092'})
    tweets = kstream.map(lambda x: x[1].encode("ascii","ignore"))
    print  tweets
    #reviews = sc.parallelize(tweets)

    #print reviews.collect()
    tweets_filtered = tweets.map(filterSpecChars)

    unique = tweets_filtered.map(uniqueWords)

    tweets_words = unique.flatMap(lambda word: word.split(" "))

    #import code;code.interact(local=locals())
    #print unique.collect()
    sentiment = tweets_words.map(checkWord)

    sentiment = sentiment.reduceByKey(lambda x, y : (int(x) + int(y)))

    sentiment = sentiment.filter(lambda x : x[0] != "none")

    # Let the counts variable hold the word counts for all time steps
    # You will need to use the foreachRDD function.
    # For our implementation, counts looked like:
    #   [[("positive", 100), ("negative", 50)], [("positive", 80), ("negative", 60)], ...]
    #return sentiment
    # counts = []

    # sentiment.foreachRDD(lambda t, rdd: counts.append(rdd.collect()))

    # sentiment = sentiment.updateStateByKey(updateFunction)

    sentiment.pprint()

    # return counts


if __name__=="__main__":
    main()
