from urllib.parse import quote_plus

import pymongo

username = quote_plus("db_admin")
password = quote_plus("db_admin")
cluster = "cluster0.k2trl.mongodb.net"

uri = "mongodb+srv://" + username + ":" + password + "@" + cluster

client = pymongo.MongoClient(uri)
