import ssl

from pymongo import *

# DiaPro Database
mongo_url = "hidden_link"
db_name = "diapro"
mongo_client = MongoClient(mongo_url, ssl_cert_reqs=ssl.CERT_NONE)
db = mongo_client[db_name]

# Mijn Kwik Database
mongo_url_mijnKwik = "hidden_link"
db_name = "mijn-kwik"
mongo_client = MongoClient(mongo_url_mijnKwik, ssl_cert_reqs=ssl.CERT_NONE)
db_mijnKwik = mongo_client[db_name]
