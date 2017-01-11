from cassandra.cluster import Cluster
import operator
import datetime,time
from kafka import KafkaProducer

cluster = Cluster(
    contact_points=['152.46.19.234'],
    )
session = cluster.connect('aniket')
producer = KafkaProducer(bootstrap_servers='152.46.16.173:9092',value_serializer=lambda v: v.encode('utf-8'))


def set_log(type_of_log, topic, string):
    #if type_of_log == "INFO":
        #type_of_log = 'logs'
    """Print DB Failures"""
    #with open("db_failure_logs.txt", "a") as myfile:
    ts = time.time()
    ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    #myfile.write("["+ts+"] : ["+type_of_log +"] :"+string+"\n")
    #log_msg = "[" + ts + "] : [" + type_of_log + "] :" + string
    log_msg = "[" + ts + "] : [" + type_of_log + "] :" + string
    try:
        #print ("Sending log :", log_msg)
        if topic == 'logs': producer.send('logs', log_msg)
        if topic == 'debug': producer.send('debug', log_msg)
    except:
        print ("Exception in sending to Kafka \n Check if Kafka Cluster working")
    return
