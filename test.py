#!/usr/bin/python

# import the Looker and Request classes #
from request import Request
from looker import Looker

# instantiate Looker and run the setup function #
Looker().setup(token = 'Mkz9GRYoIhyuJ898YG89Ig', 
						secret = 'v1+MNxMg1vdmljYbtBhEDFEQSlAUEZd4xWd', 
						host = 'https://demo.looker.com'
					)

# instantiate Request and run the query function #
myQuery = Request().query(query = 'orders', 
					dictionary = 'thelook', 
					fields = ['orders.count', 'users.count'], 
					filters = {'users.state':'-%New%', 'orders.created_date':'90 days'}
					)

anotherQuery = Request().query(query = 'orders', 
					dictionary = 'thelook', 
					fields = 'orders.count', 
					filters = {'users.created_date':'90 days', 'orders.created_date':'90 days'}
					)

print myQuery
print anotherQuery