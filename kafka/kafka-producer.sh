KA=/home/adhuri/kafka_2.11-0.10.1.0

echo "Topics on the kafkaserver "
$KA/bin/kafka-topics.sh --list --zookeeper localhost:2181

echo " write to topic google_places"
$KA/bin/kafka-console-producer.sh --broker-list 152.46.16.173:9092 --topic google_places


