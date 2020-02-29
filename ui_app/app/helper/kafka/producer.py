import traceback
from kafka import KafkaProducer

class CustomKafkaProducer():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.__producer = self.__connect()
        
    def __connect(self):
        producer = None
        try:
            connection_string = ':'.join([self.ip, self.port])
            connection_servers = [connection_string]
            producer = KafkaProducer(bootstrap_servers=connection_servers)
        except Exception as ex:
            print('Exception while connecting to Kafka producer')
            print(str(ex))
        return producer
    
    def put(self, topic_name, key, value):
        
        try:
            self.__producer.send(topic_name, key=str(key), value=str(value))
            self.__producer.flush()
            success_string = 'Pid with value {} added successfully.'.format(value)
            print(success_string)
            
        except Exception as error:
            error_string = 'Error in adding Pid {} to producer.'.format(value)
            print(error_string)
            traceback.print_exc()
