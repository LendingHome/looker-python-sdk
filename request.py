token = "Mkz9GRYoIhyuJ898YG89Ig"
secret = "v1+MNxMg1vdmljYbtBhEDFEQSlAUEZd4xWd"

key = "Mkz9GRYoIhyuJ898YG89Ig&v1+MNxMg1vdmljYbtBhEDFEQSlAUEZd4xWd"

# required libraries #
import urllib2
from hashlib import sha1
import datetime as dt
import random as rnd

class Request(object):

	# initialize the class using a constructor #
	def __init__(self, options):
		self.options = options	


	def run(dictionary, query, filters, output = 'json', method = 'GET'):

		uri = '/api/dictionaries/' + dictionary + '/' + 'queries' + '/' + query + '.' + output

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


	def generateStringToSign(method, location, today, nonce, params = {}):
		stringToSign = method + "\n"
	    stringToSign += location + "\n"
	    stringToSign += today + "\n"
	    stringToSign += nonce + "\n"

      # TODO splitting on '&' only works for GET params
      # params.inject({}) { |h, (k, v)| h[k.to_s.downcase] = v; h }.sort.each do |k,v|
      #   stringToSign += "#{k}=#{v.to_s}\n"
      # end
      
      hashed = hmac.new(secret, unicode(stringToSign, "utf-8"), sha1)

      signature =  binascii.b2a_base64(hashed.digest())[:-1]
