import os, sys, glob, pickle

sys.path.insert(1, '/home/nitin/code/Ashrut/compass/ui_app/app/helper/kafka')
from producer import CustomKafkaProducer as kafka_producer

class ProcessHandler(object):
	def __init__(self, data_folder):
		self.data_folder = data_folder
		self.kafka_producer = None

	def read_file(self, filepath):
		data = []

		with open(filepath,'r') as output_file:
			data = pickle.load(output_file)
		
		return data

	def get_process_filepaths(self, process_id):
		data_folder = '/'.join([self.data_folder, process_id, '*'])
		output = {}
		for path in glob.glob(data_folder):
			extension = path.split('.')[-1]
			output[extension] = path

		return output

	def get_all_process_ids(self):
		data_folder = self.data_folder + '/*'
		process_ids = []

		for path in glob.glob(data_folder):
			folder_name = path.split('/')[-1]
			process_ids.append(folder_name)


		return process_ids

	def get_process_name_description(self, process_id):
		info_filepath = '/'.join([self.data_folder, process_id, process_id + '.info'])
		with open(info_filepath, 'rb') as f:
			data = pickle.load(f)
		return data

	def update_file_data(self, filepath, data):
		with open(filepath, 'wb') as file_handler:
			pickle.dump(data, file_handler, protocol=pickle.HIGHEST_PROTOCOL)

	def get_process_data(self,  process_id):

		process_meta_data = self.get_process_name_description(process_id=process_id)
		process_data = {
			'pid': process_meta_data['process_id'],
			'name': process_meta_data['process_name'],
			'description': process_meta_data['process_description'],
			'timestamp': process_meta_data['timestamp']
		}
		process_filepaths = self.get_process_filepaths(process_id=process_id)
		if ('py' in process_filepaths) and (os.path.exists(process_filepaths['py'])):
			process_data['show_file_upload'] = False
			process_data['show_script_runner'] = False
		else:
			process_data['show_script_runner'] = True
			process_data['show_file_upload'] = True

		return process_data


	def get_process_status(self, process_id):
		status_filepath = '/'.join([self.data_folder, process_id, process_id+'.status'])
		if os.path.exists(status_filepath):
			return self.read_file(filepath=status_filepath)
		else:	
			return 'under_process'

	def get_all_process_data(self):
		data_folder = self.data_folder + '/*'
		running_process_data = []
		under_process_data = []
		finished_process_data = []
		process_data = {}
		for path in glob.glob(data_folder):
			folder_name = path.split('/')[-1]
			process_data = self.get_process_name_description(folder_name)

			item = {
				'pid': process_data['process_id'],
				'timestamp': process_data['timestamp'],
				'name': process_data['process_name'],
				'description': process_data['process_description'],
				'status': 'success',
				'html_url': 'http://localhost:5000/process/' + folder_name
			}

			status = self.get_process_status(folder_name)
			
			if status.lower() == 'running':
				running_process_data.append(item)
			elif status.lower() == 'under_process':
				under_process_data.append(item)
			else:
				finished_process_data.append(item)

		return running_process_data, under_process_data, finished_process_data

	def push_to_kafka(self, process_id, ip, port, topic_name):
		value = process_id
		key = process_id

		if self.kafka_producer is None:
			self.kafka_producer = kafka_producer(ip=ip, port=port )
		self.kafka_producer.put(topic_name= topic_name, key=key, value=value)

		return True
