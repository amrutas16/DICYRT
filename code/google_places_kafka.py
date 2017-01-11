from google_places import get_place_details,get_place
from kafka import KafkaProducer
import json

# p = get_place('RockysLounge','40.3964688,-80.0849416')



def create_list_for_kafka(business_id,name,location):
	p=get_place(name,location)
	
	js= get_place_details(p)
	lists=[]
	for i in js['reviews']:
		 i['business_id']=business_id
		 lists.append(i)	
	print "List is ",lists
	return lists


def main(business_id, restaurant_name, location):
	try:
		producer = KafkaProducer(bootstrap_servers='152.46.16.173:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))
		
		for i in create_list_for_kafka(business_id, restaurant_name, location):
			print ("Sending :", i)
			producer.send('google_places', i)
			print ("\nSent")
			
	except Exception as e:
		print ("Exception in sending to Kafka \n Check if Kafka Cluster working ",e)

if __name__=="__main__":
	#main('ASidDajshf','RockysLounge','40.3964688,-80.0849416')
	#main('ASifDajshf','Arizona Pizza Company','33.65379,-112.23381')

	#main('Afsgghh','Hummus Xpress','33.4078,-111.95375')
	#main('Acsgghh','IHOP','33.42348,-111.92575')
	main('Bcvgghw','Fatburger','33.42596,-111.94025')
