# required libraries #
from array import array
import urllib
from hashlib import sha1
import datetime as dt
import random as rnd
import requests
import base64
import hmac
import binascii
import looker

class Request(object):

	# initialize the class using a constructor #
	def __init__(self):
		pass

	# define query method, which contructs and makes the GET request #
	def query(self, query, dictionary, fields, filters = None, output = 'json', method = 'GET'):

		# from Looker().setup, get token, secret, and host #
		token = looker.values['token']
		secret = looker.values['secret']
		host = looker.values['host']

		if isinstance(fields, str):
		    fields = fields.split()
		elif isinstance(fields, type({})):
		    raise TypeError('Fields must be a list or a string')
		else:
		    pass		

		uri = '/api/dictionaries/' + dictionary + '/' + 'queries' + '/' + query + '.' + output
		params = {}
		params['fields'] = fields
		if filters is not None:
			params['filters'] = filters
		else:
			pass
		query_params = self.__buildQueryParams(params)

		# create inputs for GET header # 
		today = dt.datetime.now().strftime('%a, %d %b %Y %H:%M:%S -0800')
		nonce = hex(rnd.getrandbits(128))[2:-1]
		stringToSign = self.__generateStringToSign(method, uri, today, nonce, query_params)
		hashed = hmac.new(secret, unicode(stringToSign, "utf-8"), sha1)
		signature =  binascii.b2a_base64(hashed.digest())[:-1]

		# create header #
		header = {}
		header["Authorization"] = token + ':' + signature
		header["Date"] = today
		header["x-llooker-nonce"] = nonce
		header["Accept"] = "application/json"
		header["x-llooker-api-version"] = 1

		url = host + uri + '?' + query_params

		r = requests.get(url, headers=header)
		return r.text

	# __buildQueryParams is a private function that puts fields and filters into 
	# the proper format to make a Looker API call #
	def __buildQueryParams(self, params):
		filter_list = []
		for m in params.itervalues():
			if isinstance(m, type([])):
				field_list = sorted([i.lower() for i in m])
				field_list = ','.join(str(i) for i in field_list)
				field_list = 'fields=' + field_list
			elif isinstance(m, type({})):
				for k, v in m.items(): 
					filter_list.append('filters[' + str(k).lower()  + ']=' + urllib.quote_plus(str(v)))
			else:
				print "Your input is neither an array of fields nor a hash of filters."	
		if filter_list != []:
			return field_list + '&' + '&'.join(i for i in filter_list)
		else:
			return field_list
	
	#__generateStringToSign is a private function that #
	def __generateStringToSign(self, method, uri, today, nonce, query_params):
		stringToSign = method + "\n" + uri + "\n" + today + "\n" + nonce + "\n" + query_params.replace('&', "\n") + "\n"
		return stringToSign