Looker SDK for Python
===========================

A Python library for Lookers's HTTP-based APIs.

- https://github.com/sdhoover/Python_SDK

Setup
-----

You can install this package by cloning this directory and running:

   ```$ python setup.py install```

Getting Looker API keys
-----------------------

Within your Looker, navigate to admin, manager users, then either create a new API user or get the token and secret associated with an existing API user.


Using the Looker Python SDK
---------------------

    from looker.client import LookerClient

    # instantiate LookerClient
    client = LookerClient('<token>',
                          '<secret>',
                          'https://<company_name>.looker.com')

    # create a query object
    query1 = client.query(dictionary = 'thelook',                               # this is the model
                          query = 'orders',                                     # this is the base view
                          fields = ['orders.count', 'users.count'],             # dimensions and measures
                          {'users.state': '-%New%',
                           'orders.created_date': '90 days'})                   # filters as key-value pairs

    # create another query object
    query2 = client.query('thelook', 'orders', 
                          ['orders.count'],
                          {'users.created_date': '90 days'})
    query2.add_filters({'orders.created_date': '90 days'})                      # you can add filters post query build

    print query1.run()
    print query2.run()
