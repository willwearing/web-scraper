import re
from pymongo import MongoClient
import certifi
import urllib.parse

my_dict = { "url": '', "data": '' }

def load_data(url, json_blob):
    # Login creds for database user
    with open("token") as t:
      token = t.read()
    token_list = re.split('; |, |\*|\n', token)
    username = urllib.parse.quote_plus(token_list[0])
    password = urllib.parse.quote_plus(token_list[1])

    # Database connection string
    client = MongoClient('mongodb+srv://%s:%s@cluster0.dw9d6.mongodb.net/myFirstDatabase' % (username, password), tlsCAFile=certifi.where())

    db = client['myFirstDatabase']

    # Replace string with targetted collection

    coll = db.get_collection('testCollection')

    my_dict['url'] = url
    my_dict['data'] = json_blob

    if '_id' in my_dict: 
        del my_dict['_id']

     # To insert a single dictionary at a time. Can be built written too
    coll.insert_one(my_dict)
