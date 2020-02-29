import os, sys

class ScriptRunner(object):
	def __init__(self):
		pass

	def run_script(self, script_filepath, log_filepath):
		try:
			command = 'python {} > {}'.format(script_filepath, log_filepath)
			os.system(command)
		except Exception as e:
			print ('---------------------------------')
			print ('ERROR while running the command!')
			print ('command: ' + command)
			print ('error: ' + str(e))
			print ('---------------------------------')