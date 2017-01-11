from cassandra.cluster import Cluster 
import operator
import datetime,time
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement, dict_factory, named_tuple_factory
import config,json
from kafka import KafkaProducer
from setting_logs import set_log

import socket

cluster = Cluster(
	contact_points=['152.46.19.234'],
	)
session = cluster.connect('aniket')

try:
	producer = KafkaProducer(bootstrap_servers='152.46.16.173:9092',value_serializer=lambda v: v.encode('utf-8'))
except Exception as e:
	#print "Cannot connect ", str(e) 
	set_log("ERROR", "debug", "Retrying connect to Kafka from "+str(socket.gethostname()))


def get_food_details(b_id,top=10):
	global session
	#setLog("INFO","Getting food_details for business_id = " + b_id +", count "+str(top))
	set_log("INFO", "logs", "Getting food_details for business_id = " + b_id +", count "+str(top))
	get_result_prepared = session.prepare("select business_id,food,count from food_details where business_id=? ")
	results = session.execute(get_result_prepared,[b_id])
	return getDict(b_id,results,top)


def getDict(b_id,results,top):
	dic={}
	for result in results:
		if result.food in dic:
			dic[result.food]+= result.count
		else:
			dic[result.food] = result.count
	#print dic
	sorted_x = sorted(dic.items(), key=operator.itemgetter(1),reverse=True)
	dic2={}
	dic2['food_list'] = sorted_x[:top]
	dic2['business_id'] = b_id
	return dic2


def get_foodcounts(food, business_id):
       try:
           msg = "Getting food_details for business_id " + str(business_id) + " and food " + str(food)
           set_log("INFO", "debug", msg)
           #print "After set_log"
           get_foodcounts_prepared = session.prepare("select count from food_details where business_id=? and food=?")
           result = session.execute(get_foodcounts_prepared, (business_id, food))
           food_count = result[0].count
           msg = "The count for " + str(business_id) + " and " + str(food) + " is " + str(food_count)
           set_log("INFO", "debug", msg)
           return food_count
       except Exception as e:
           msg = "Food" + str(food) +" does not appear in the review for " + str(business_id)
           set_log("INFO", "debug", msg)
           return 0
       #print food_count

def get_business_details(city): 
        try:
            set_log("INFO", "debug", "Getting business details for city " + str(city))
            #print "After set log in business details"
            get_business_details_prepared = session.prepare("select name, business_id, full_address, latitude, longitude, stars from business_details where city=?")
            session.row_factory = dict_factory
            results = session.execute(get_business_details_prepared, [city])
            session.row_factory = named_tuple_factory
            result_list = [i for i in results]
            set_log("INFO", "debug", "The business details for city " + city + " are " + repr(result_list))
            return result_list
        except Exception as e:
			 #setLog("ERROR","Failed to get business details for city " + str(city))
             set_log("ERROR", "debug", "Failed to get business details for city " + str(city))
            

def get_business_details_for_kafka(business_id):
        business_id = business_id.strip()
        get_business_details_prepared = session.prepare("select name, latitude, longitude from business_details where business_id=? ALLOW FILTERING")
        session.row_factory = dict_factory
        results = session.execute(get_business_details_prepared, [business_id])
        session.row_factory = named_tuple_factory
        result_list = [i for i in results]
        return result_list


def get_top_restaurants(food, city):
        limit = 10
        business_details = get_business_details(city)
        #print 'The business details are: ', repr(business_details)
        #print len(business_details)
        top_restaurants = []
        if len(business_details) == 0:
            set_log("ERROR", "logs", "Could not get business details for " + str(city) + " and " + str(food))
            return []
        for business in business_details:
            #print business
            count = int(get_foodcounts(food, str(business['business_id'])))
            if count > 0:
                business['count'] = count
                top_restaurants.append(business)
        top_restaurants = sorted(top_restaurants, key=lambda restaurant: restaurant['count'], reverse=True)
        #print 'The top restaurants are: ' , repr(top_restaurants)
        l = len(top_restaurants)
        if l < limit:
            limit = l
        #print top_restaurants[:limit] 
        return top_restaurants[:limit] 
            

def insert_food_details(element,source):
	try:	
		element['source']=source
		#setLog("INFO", " Inserting into food_details :" + str(element))
		set_log("INFO", "debug", "Inserting into food_details :" + str(element))
		session.execute(
		"""
    		INSERT INTO food_details (business_id, food, count, source)
    		VALUES (%(business_id)s, %(food)s, %(count)s, %(source)s)
    		""",element)
	except:
		#setLog("ERROR", " Failed inserting into food_details :" + str(element))
		set_log("ERROR", "logs", " Failed inserting into food_details :" + str(element))


def get_business_id(name,city):
	#setLog("INFO","Getting  business_id for name : " + name +", city :  "+city)
	set_log("INFO", "logs", "Getting  business_id for name : " + name +", city :  "+city)
	get_businessid_prepared = session.prepare("select business_id from business_details where name=? and city=? ")
	results = session.execute(get_businessid_prepared,(name,city))
	#print results[0]
	try:
		if results[0].business_id:
			return results[0].business_id
		else: 
			return None
	except:
		return None


def insert_business_details(business_list):
	try:	
    		with open(business_list) as f:
        		content = f.readlines()
        		#print content
        		a= json.loads(json.dumps(content))

    			count=0
    			for i in a:
        			b=json.loads(i)
        			mydict={}
        			for j in ['business_id','name','city','state','full_address','latitude','longitude','stars']:
            				mydict[j]=b[j]
        			#print "db.business.insert( ",mydict," )"
				"""
				"""
				if (mydict['city']):
        				count+=1
					session.execute(
             				"""
                			INSERT INTO business_details (business_id,name,city,state,full_address,latitude,longitude,stars)
                			VALUES (%(business_id)s, %(name)s, %(city)s, %(state)s , %(full_address)s, %(latitude)s, %(longitude)s,%(stars)s)
                			""",mydict)
        				#setLog("INFO","Insert Done : "+ mydict['business_id']+"\t"+mydict['name'])
        				set_log("INFO", "debug", "Insert Done : "+ mydict['business_id']+"\t"+mydict['name'])
    			#setLog("INFO","Inserted "+str(count)+" number of businesses ")


	except Exception as e:
		#setLog("ERROR", " Failed inserting into business_details : " +str(e))
		setLog("ERROR", "logs", " Failed inserting into business_details : " +str(e))


def setLog(type_of_log,string):
        if type_of_log == "INFO":
         type_of_log = 'logs'
	"""Print DB Failures"""
	#with open("db_failure_logs.txt", "a") as myfile:
	ts = time.time()
	ts=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	#myfile.write("["+ts+"] : ["+type_of_log +"] :"+string+"\n")
	m = "[" + ts + "] : [" + type_of_log + "] :" + string
	try:
		print ("Sending :", m)
		if type_of_log == 'logs': producer.send('logs', m)
		if type_of_log == 'debug': producer.send('debug', m)
		print ("\nSent")			
	except:
		print ("Exception in sending to Kafka \n Check if Kafka Cluster working")
    #print ("["+ts+"] : ["+type_of_log +"] :"+string+"\n")
	#"""

	
if __name__=='__main__':
	#print get_food_details('xyz')
	#e={'food': u'sandwich', 'count': 4, 'business_id': u'fDC3yJqfHFq2bJ8D4F535w'}
	#insert_food_details(e,"Yelp")
	
	#insert_business_details(config.businesslist)

	#get_business_id("Bear Creek Golf Complex","Chandler")
        #get_business_details('Goodyear')
    get_top_restaurants('Tacos', 'Goodyear')
