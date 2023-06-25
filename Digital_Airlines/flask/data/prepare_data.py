import json, os, sys
from pymongo import MongoClient

mongodb_hostname = os.environ.get("MONGO_HOSTNAME","localhost")
client = MongoClient('mongodb://'+mongodb_hostname+':27017/')

db = client["DigitalAirlines"]
collUsers = db["AirlineUserCollection"]


def insert_all():
    file = open('./data/users.json','r')
    lines = file.readlines()
    for line in lines:
        entry = None 
        try:
            entry = json.loads(line)
        except Exception as e:
            print(e)
            continue
        if entry != None:
            entry.pop("_id",None) 
            try:
                collUsers.insert_one(entry)
            except Exception as e:
                print(e)

