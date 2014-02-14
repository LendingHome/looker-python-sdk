import urllib
from hashlib import sha1
import datetime as dt
import random as rnd
import requests
import base64
import hmac
import binascii


class LookerClient(object):

	def __init__(self, token, secret, host, port=443):
		self.token = token
		self.secret = secret
		self.host = host
		self.port = port

	def query(self, query, dictionary, fields, filters=None, output='json', method='GET'):
		return Query(self, query, dictionary, fields, filters=filters, output=output, method=method)


class Query(object):

	filters = {}

	# no support for method != GET
	def __init__(self, credentials, query, dictionary, fields, filters=None, output='json', method='GET'):
		self.credentials = credentials
		self.query = query
		self.dictionary = dictionary
		self.fields = fields
		self.output = output
		self.method = method
		self.add_filters(filters)

	def run(self):
		uri = "/api/dictionaries/%s/queries/%s.%s" % (self.dictionary, self.query, self.output)
		url = "%s%s?%s" % (self.credentials.host, uri, self.__query_params())
		r = requests.get(url, headers=self.__headers(uri))
		return r.text

	def add_filters(self, filters):
		if filters is not None:
			self.filters.update(filters)
		return self

	def __query_params(self):
		fields_string = ",".join(sorted([field.lower() for field in self.fields]))
		filters_list = []
		for key, value in self.filters.iteritems():
			filters_list.append("filters[%s]=%s" % (str(key).lower(), urllib.quote_plus(str(value))))
		return "fields=%s&%s" % (fields_string, "&".join(filters_list))

	def __headers(self, uri):
		today = dt.datetime.now().strftime('%a, %d %b %Y %H:%M:%S -0800')
		nonce = hex(rnd.getrandbits(128))[2:-1]
		stringToSign = self.__generateStringToSign(self.method, uri, today, nonce)
		hashed = hmac.new(self.credentials.secret, unicode(stringToSign, "utf-8"), sha1)
		signature =  binascii.b2a_base64(hashed.digest())[:-1]
		return {"Authorization": self.credentials.token + ':' + signature,
		        "Date": today,
				"x-llooker-nonce": nonce,
				"Accept": "application/json",
				"x-llooker-api-version": 1})
	
	# creates StringToSign, which goes in the header signature
	def __generateStringToSign(self, uri, today, nonce):
		fields = [self.method,                                 
		          uri,
		          today,
		          nonce,
		          self.__query_params().replace('&', "\n")]             
		return "\n".join(fields) + "\n"
