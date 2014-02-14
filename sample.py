#!/usr/bin/python

from looker import LookerClient

# instantiate LookerClient
client = LookerClient('Mkz9GRYoIhyuJ898YG89Ig',
                      'v1+MNxMg1vdmljYbtBhEDFEQSlAUEZd4xWd',
                      'https://demo.looker.com')

# create a query object
query1 = client.query('orders',
                      'thelook',
                      ['orders.count', 'users.count'],
                      {'users.state': '-%New%',
                       'orders.created_date': '90 days'})

query2 = client.query('orders', 'thelook', ['orders.count'],
                      {'users.created_date': '90 days',
                       'orders.created_date': '90 days'})

print query1.run()
print query2.run()
