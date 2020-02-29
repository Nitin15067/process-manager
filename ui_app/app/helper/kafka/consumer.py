from kafka import KafkaConsumer
import time, sys, os

sys.path.insert(1, '/home/nitin/code/Ashrut/compass/ui_app/app/config')
from config_reader import ConfigReader

# sys.path.insert(1, '/home/nitin/code/Ashrut/compass/ui_app/app/helper/handler/process')
# from process_handler import ProcessHandler

sys.path.insert(1, '/home/nitin/code/Ashrut/compass/ui_app/app/helper/file_upload')
from file_uploader import FileUploader

sys.path.insert(1, '/home/nitin/code/Ashrut/compass/ui_app/app/helper/runners')
from script_runner import ScriptRunner


script_runner = ScriptRunner()
file_uploader = FileUploader()
config = ConfigReader()
# process_handler = ProcessHandler(config.get_app_data_folder())


class CustomKafkaConsumer():
    def __init__(self, ip, port, topic, from_begin=True):
        self.topic = topic
        self.ip = ip
        self.port = port
        if from_begin:
            self.__consumer = self.__connect(auto_offset_reset='earliest')
        else:
            self.__consumer = self.__connect(auto_offset_reset='latest')
        
    def __connect(self, auto_offset_reset):
        consumer = None
        try:
            connection_string = ':'.join([self.ip, self.port])
            connection_servers = [connection_string]
            consumer = KafkaConsumer(self.topic, auto_offset_reset=auto_offset_reset,
                                     bootstrap_servers=connection_servers, consumer_timeout_ms=1000, 
                                     max_poll_records=1, fetch_max_wait_ms=1000)
        except Exception as ex:
            print('Exception while connecting to Kafka consumer')
            print(str(ex))
        return consumer
    
    def __check(self, filepath, search_str):
        with open(filepath, 'r') as ins:
            for line in ins:
                if search_str in line:
                    return True
        return False

    def get(self):
        while(True):
            for data in self.__consumer:
                pid = data.key

                status_filepath = config.get_status_filepath(pid)
                status = 'Running'
                file_uploader.update_status_file(status_filepath, status)

                script_filepath = config.get_script_filepath(pid)
                log_filepath = config.get_log_filepath(pid)

                script_runner.run_script(script_filepath, log_filepath)
                while(True):
                    output_filepath = config.get_output_filepath(pid)
                    command = 'ps aux | grep script_runner_{}.py > {}'.format(pid, output_filepath)
                    os.system(command)
                    search_str = 'python {}.py'.format(pid)
                    if not self.__check(output_filepath, search_str):
                        break

                status = 'Done'
                file_uploader.update_status_file(status_filepath, status)







                