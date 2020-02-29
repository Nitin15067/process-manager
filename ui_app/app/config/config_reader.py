import os, sys, json, shutil

class ConfigReader(object):
	def __init__(self, filepath=None):
		if filepath is None:
			filepath = '/'.join([os.path.dirname(os.path.abspath(__file__)), 'config.json'])
		self.filepath = filepath

		self.data = self.read_config()

	def read_config(self):
		with open(self.filepath) as json_data_file:
			data = json.load(json_data_file)
		return data

	def get_script_filepath(self, process_id):
		root_folder = self.data['root_folder']
		data_folder = self.data['data_folder']

		return '/'.join([root_folder, data_folder, str(process_id), 'script_runner_' + str(process_id) + '.py'])

	def get_log_filepath(self, process_id):
		root_folder = self.data['root_folder']
		data_folder = self.data['data_folder']

		return '/'.join([root_folder, data_folder, str(process_id), str(process_id) + '.log'])

	def get_status_filepath(self, process_id):
		root_folder = self.data['root_folder']
		data_folder = self.data['data_folder']

		return '/'.join([root_folder, data_folder, str(process_id), str(process_id) + '.status'])

	def get_info_filepath(self, process_id):
		root_folder = self.data['root_folder']
		data_folder = self.data['data_folder']

		return '/'.join([root_folder, data_folder, str(process_id), str(process_id) + '.info'])		

	def get_output_filepath(self, process_id):
		root_folder = self.data['root_folder']
		data_folder = self.data['data_folder']

		return '/'.join([root_folder, data_folder, str(process_id), str(process_id) + '.out'])		

	def get_process_folder(self, process_id):
		root_folder = self.data['root_folder']
		data_folder = self.data['data_folder']

		return '/'.join([root_folder, data_folder, str(process_id)])		

	def delete_process_folder(self, process_id):
		process_folder = self.get_process_folder(process_id=process_id)
		shutil.rmtree(process_folder)

	def get_process_url(self, process_id):
		home_url = self.data['home_url']

		return '/'.join([home_url, 'process', process_id])

	def get_app_data_folder(self):
		root_folder = self.data['root_folder']
		data_folder = self.data['data_folder']

		return '/'.join([root_folder, data_folder])

	def get_kafka_producer_data(self):
		return self.data['kafka']['producer']

	def get_kafka_consumer_data(self):
		return self.data['kafka']['consumer']
