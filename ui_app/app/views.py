from flask import render_template, redirect, request, Flask, session, jsonify
from werkzeug.utils import secure_filename

from app import app
import os, sys, traceback, json

# from helper.handler.main_handler import mainHandler
from app.helper.file_upload.file_uploader import FileUploader
from app.helper.handler.process.process_handler import ProcessHandler
from app.config.config_reader import ConfigReader as AppConfig
from app.helper.time.time_fetcher import TimeFetcher
from app.helper.runners.script_runner import ScriptRunner

# main_handler = mainHandler()
time_fetcher = TimeFetcher()
app_config = AppConfig()
app_file_uploader = FileUploader()
script_runner = ScriptRunner()
process_handler = ProcessHandler(app_config.get_app_data_folder())
app.secret_key = 'impicklerick'


import random, string, uuid

# def randomword(length):
#    letters = string.ascii_lowercase
#    return ''.join(random.choice(letters) for i in range(length+1))

# def random_string(length):
#   	return ' '.join([randomword(i+1) for i in range(length+1)])

# def random_output(data):
# 	return {
# 		'name': randomword(6),
# 		'discription': random_string(8),
# 		'html_url': 'http://localhost:5000/process/' + str(uuid.uuid4())
# 	}

def convert_process_data(process_data):
	output = []
	for process in process_data:
		item = {
			'pid': process['pid'],
			'timestamp': process['timestamp'],
			'name': process['name'],
			'discription': process['description'],
			'status': 'success',
			'html_url': 'http://localhost:5000/process/' + process['html_url']
		}
		output.append(item)
	return output


def get_all_process_ids():
	return []

@app.route('/')
def home():
	running_process_data, under_process_data, _ = process_handler.get_all_process_data()
	running_process_count = len(running_process_data)
	under_process_count = len(under_process_data)
	
	data={'result': {}}

	data['result']['running_process_data'] = convert_process_data(running_process_data)
	data['result']['under_process_data'] = convert_process_data(under_process_data)
	
	data['result']['over_time_processes'] = 1
	data['result']['stopped_processes'] = 0
	data['result']['running_process_count'] = running_process_count
	data['result']['under_process_count'] = under_process_count
	data['result']['url_prefix'] = 'http://localhost:5000'
	return render_template('home.html', data=data)


@app.route('/delete_process/<process_id>')
def delete_process(process_id):
	app_config.delete_process_folder(process_id=process_id)

	return redirect("http://localhost:5000")
	
@app.route('/search/<data_id>', methods=['GET'])
def autocomplete_wikth_id(data_id):
	data_id = str(data_id)
	process_data = []
	_, under_process_data, _ = process_handler.get_all_process_data()
	for process in under_process_data:
		name_description = ' '.join([process['name'],process['description']])

		if data_id.lower() in name_description.lower():
			item = {
				'name' : process['name'],
				'description' : process['description'],
				'html_url' : process['html_url'] 
			}
			process_data.append(item)
	output = {}
	output['result_data'] = process_data
	return jsonify(output)

@app.route('/new_process')
def create_new_process():
	return render_template('new_process.html', data={})

@app.route('/create_process', methods=["POST"])
def create_process():
	response = {}

	try:
		process_name = request.form['process_name']
		process_description = request.form['process_description']
		process_id = str(uuid.uuid4())
		data = {
			'process_name': process_name,
			'process_description': process_description,
			'process_id': process_id,
			'timestamp': time_fetcher.get_current_timestamp(pattern='dd MM, yy hh:mm:ss p')
			# 'timestamp' : '',
		}
		
		info_filepath = app_config.get_info_filepath(process_id=process_id)
		app_file_uploader.check_and_create_dir(path=info_filepath)
		process_handler.update_file_data(filepath=info_filepath, data=data)
		response['process_url'] = app_config.get_process_url(process_id=process_id)

		response['status'] = True
	except Exception as error:
		response = {
			'status': False,
			'error': str(traceback.format_exc())
		}
	return jsonify(response)

@app.route('/process/<process_id>')
def get_process(process_id):
	response = {}
	p_id = str(process_id)
	all_process_ids = process_handler.get_all_process_ids()
	process_status = process_handler.get_process_status(p_id)
	print(process_status)
	if p_id in all_process_ids:
		response = process_handler.get_process_data(process_id=p_id)
		response['status'] = process_status.lower()
	else:
		response = {
			'pid': p_id,
			'name': 'ErrorName',
			'description': 'ErrorDescription',
			'show_runner_message': False,
			'show_script_runner': True
			}
	print(response)
	return render_template('process.html', data=response)

@app.route('/finished_process')
def get_finished_process():
	_, _, finished_process_data = process_handler.get_all_process_data()
	finished_process_count = len(finished_process_data)
	data={'result': {}}
	data['result']['finished_process_data'] = convert_process_data(finished_process_data)
	data['result']['over_time_processes'] = 1
	data['result']['stopped_processes'] = 0
	data['result']['url_prefix'] = 'http://localhost:5000'
	data['result']['finished_process_count'] = finished_process_count
	return render_template('finished_process.html', data=data)

@app.route('/process_history')
def get_process_history():
	return render_template('process_history.html', data={})

@app.route('/upload/<process_id>', methods = ['POST'])
def upload_file(process_id):
	try:
		process_id = str(process_id)
		if request.method == 'POST':
			file = request.files['file']
			script_filepath = app_config.get_script_filepath(process_id=process_id)
			app_file_uploader.check_and_create_dir(path=script_filepath)
			file.save(script_filepath)
			script_data = app_file_uploader.read_script(filepath=script_filepath)

			return jsonify({'status': True, 'script_data': script_data})
	except Exception as error:	
		return jsonify({'status': False, 'error': str(error), 'message': 'Unable to fetch the file.'})

@app.route('/get_script', methods=["POST"])
def get_script():
	try:
		response = {}
		if request.method == 'POST':
			process_id = request.form['process_id']
			script_filepath = app_config.get_script_filepath(process_id=process_id)
			script_data = app_file_uploader.read_script(filepath=script_filepath)
			response['script_data'] = script_data
		response['status'] = True
	except Exception as error:
		response = {
			'status': False,
			'error': str(traceback.format_exc())
		}
	
	return jsonify(response)

@app.route('/get_logs', methods=["POST"])
def get_logs():
	try:
		response = {}
		if request.method == 'POST':
			process_id = request.form['process_id']
			log_filepath = app_config.get_log_filepath(process_id=process_id)
			script_data = app_file_uploader.read_script(filepath=log_filepath)
			response['script_data'] = script_data
		response['status'] = True
	except Exception as error:
		response = {
			'status': False,
			'error': str(traceback.format_exc())
		}
	
	return jsonify(response)

@app.route('/run_script', methods=['POST'])
def run_script():

	try:
		response = {}
		if request.method == 'POST':
			process_id = request.form['process_id']
			script_data = request.form['script_data']
			script_data = str(script_data).split('\n')

		#creating the py file
			script_filepath = app_config.get_script_filepath(process_id=process_id)
			app_file_uploader.update_file_data(filepath=script_filepath, data=script_data)

		#sending pid to queue
			data = app_config.get_kafka_producer_data()
			ip = data['ip']
			port = data['port']
			topic = data['topic']
			push_to_kafka = process_handler.push_to_kafka(process_id, ip, port, topic)

			# start_kafka_consumer = process_handler.start_kafka_consumer()
			
			# log_filepath = app_config.get_log_filepath(process_id=process_id)
			# script_runner.run_script(script_filepath=script_filepath, log_filepath=log_filepath)
			
			# status_filepath = app_config.get_status_filepath(process_id=process_id)
			# script_runner.create_status_file(script_filepath=script_filepath, status_filepath=status_filepath)
			

		response['status'] = True
	except Exception as error:
		response = {
			'status': False,
			'error': str(traceback.format_exc())
		}
	
	return jsonify(response)

