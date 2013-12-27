#!/usr/bin/python

# required libraries #
from array import array
import urllib2
from hashlib import sha1
import datetime as dt
import random as rnd
import requests
import base64
import hmac
import binascii

class Request(object):

	# initialize the class using a constructor #
	def __init__(self):
		pass		

	# define run method, which contructs and makes the GET request #
	def run(self, fields, filters = None, output = 'json', method = 'GET'):

		# need token, secret, dictionary, and query to be passed into another 
		# Looker.function and passed into Request.run as variables
		token = "Mkz9GRYoIhyuJ898YG89Ig"
		secret = "v1+MNxMg1vdmljYbtBhEDFEQSlAUEZd4xWd"
		dictionary = 'thelook'
		query = 'orders'

		# host should be passed into Request.run from Looker.setup 
		host = 'https://demo.looker.com'

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
	
	#__generateStringToSign is a private function that #
	def __generateStringToSign(self, method, uri, today, nonce, query_params):
		stringToSign = method + "\n" + uri + "\n" + today + "\n" + nonce + "\n" + query_params.replace('&', "\n") + "\n"
		return stringToSign

