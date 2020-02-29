import sys

sys.path.insert(1, '/home/nitin/code/Ashrut/compass/ui_app/app/helper/kafka')
from consumer import CustomKafkaConsumer as kafka_consumer
from config.config_reader import ConfigReader

config = ConfigReader()
data = config.get_kafka_consumer_data()


ip = data['ip']
port = data['port']
topic = data['topic']

from_begin = True
if data['from_begin'] == 0:
	from_begin = False

consumer = kafka_consumer(ip=ip, port=port, topic=topic, 
						  from_begin=from_begin)
print('Starting Kafka Consumer!')
consumer.get()