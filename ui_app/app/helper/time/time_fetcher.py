import os, sys, datetime

class TimeFetcher(object):
	def __init__(self):
		pass

	def get_current_timestamp(self, pattern=None):
		if pattern is None: 
			return None

		if pattern == 'dd MM, yy hh:mm:ss p':
			current_date = datetime.datetime.now().strftime("%d %b, %Y")
			current_time = datetime.datetime.now().strftime("%I:%M:%S %p")

			return ' '.join([current_date, current_time])

if __name__ == '__main__':
	tf = TimeFetcher()
	pattern= 'dd MM, yy hh:mm:ss p'
	print (tf.get_current_timestamp(pattern=pattern))