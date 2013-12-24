#!/usr/bin/python

# required libraries #
import urllib2
from hashlib import sha1
import datetime as dt
import random as rnd

class Request(object):

	# initialize the class using a constructor #
	def __init__(self, options):
		self.options = options	


	def run(fields, filters = None, output = 'json', method = 'GET'):

		uri = '/api/dictionaries/' + dictionary + '/' + 'queries' + '/' + query + '.' + output
		params = {}
		params['fields'] = fields
		if filters is not None:
			params['filters'] = filters
		else:
			pass
		query_params = buildQueryParams(params)

		# create inputs for GET header # 
		today = dt.datetime.now().strftime('%a, %d %b %Y %H:%M:%S -0800')
		nonce = hex(rnd.getrandbits(128))[2:-1]
		signature = generateStringToSign(method, uri.path, today, nonce, query_params)

		# create header #
		header = {}
		header["Accept"] = "application/json"
		header["Date"] = today
		header["x-llooker-nonce"] = nonce
		header["Authorization"] = token + ':' + signature


	# if parameters are fields
	# 1. all characters to lowercase
	# 2. sort array of strings alphabetically
	# 3. turn array into a comma-separated list
	# else if parameters are filters
	def buildQueryParams(params):
		for m in params.itervalues():
			if isinstance(m, type([])):
				field_list = sorted([i.lower() for i in m])
				field_list = ','.join(str(i) for i in field_list)	
				field_list = 'fields=' + field_list
			elif isinstance(m, type({})):
				filter_list = []			
				for k, v in m.items(): 
					filter_list.append('filters[' + str(k).lower()  + ']=' + str(v).lower().replace(' ', '+'))
			else:
				print "Your input is neither an array of fields nor a hash of filters."	
		return field_list + '&' + '&'.join(i for i in filter_list)			
	

	def generateStringToSign(method, location, today, nonce, params = {}):
		stringToSign = method + "\n"
	    stringToSign += location + "\n"
	    stringToSign += today + "\n"
	    stringToSign += nonce + "\n"

	    # insert part to split query_params on &

    	hashed = hmac.new(secret, unicode(stringToSign, "utf-8"), sha1)
    	signature =  binascii.b2a_base64(hashed.digest())[:-1]

