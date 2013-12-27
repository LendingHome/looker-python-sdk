class Looker:

	def __init__(self):
		pass

	def setup(self, token = None, secret = None, host = None, port = 443):
		values = {}
		values['token'] = token
		values['secret'] = secret
		values['host'] = host
		values['port'] = port

