KA=/home/adhuri/kafka_2.11-0.10.1.0

$KA/bin/kafka-server-start.sh $KA/config/server.properties&

$KA/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic google_places
