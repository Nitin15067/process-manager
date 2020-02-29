import os, sys, pickle


class FileUploader(object):
	def __init__(self):
		pass

	def check_and_create_dir(self, path):
		directory = os.path.dirname(path)
		if not os.path.exists(directory):
			os.makedirs(directory)

	def read_script(self, filepath):
		data = []
		if os.path.exists(filepath):
			file = open(filepath)
			for line in file:
				data.append(line)
			file.close()

		return data

	def update_file_data(self, filepath, data):
		script_file = open(filepath, 'w')
		for line in data:
			script_file.write(line + '\n')
		script_file.close()

	def update_status_file(self, filepath, status):
		with open(filepath,'wb') as output_file:
			pickle.dump(status, output_file, protocol=pickle.HIGHEST_PROTOCOL)
		output_file.close()