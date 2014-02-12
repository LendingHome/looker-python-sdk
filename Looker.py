values = {}
class Looker(object):

	# initialize the class using a constructor #
	def __init__(self):
		pass

	# pass token, secret, host, and port as global variables for use in subsequent queries #
	def setup(self, token = None, secret = None, host = None, port = 443):
		global values
		values['token'] = token
		values['secret'] = secret
		values['host'] = host
		values['port'] = port
		return values