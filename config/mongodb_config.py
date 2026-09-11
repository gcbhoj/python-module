from pymongo import MongoClient
from config.envconfig import ATLAS_URI

def connect_mongodb():
    client = MongoClient(ATLAS_URI)
    # print("ATLAS_URI =", ATLAS_URI)
    return client["my-app"]