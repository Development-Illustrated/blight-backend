from pymongo import MongoClient
import time
import json
from pprint import pprint
import logging
logger = logging.getLogger("blight")

def get_user_info(userid):
    db = MongoClient().get_database("blight")
    userInfo = db.users.find_one({"userid":userid})
    if userInfo:
        return userInfo
    else:
        return False

# print(get_user_info("virusman"))

def create_user_info(userid, team):
    db = MongoClient().get_database("blight")
    userExists = db.users.find({"userid":userid}).count()
    if userExists:
        logger.warning(userid + " already exists")
        return(get_user_info(userid))

    else:
        logger.info("Creating new user:")
        defBalance="1"
        defMinersActiveInventoryLimit="5"
        defMinersInactiveInventoryLimit="10"
        defRadius="100"
        lastSeen=int(time.time())        
        userInfo = { 
            "userid" : userid,
            "lat" : "0",
            "lng" : "0",
            "balance" : defBalance,
            "team" : team,
            "minersInactiveInventoryLimit" : defMinersInactiveInventoryLimit,
            "minersActiveInventoryLimit" : defMinersActiveInventoryLimit,
            "minersInactiveInventory" : store_items_load(),
            "minersActiveInventory" : store_items_load(),
            "radius" : defRadius,
            "lastSeen" : lastSeen
        }
        response = db.users.insert(userInfo)
        logger.info("Response from mongo: " +str(response))

        return(get_user_info(userid)) 

# print(create_user_info('virusmansd2', "red"))

def update_user_info(userid, user_obj):
    db = MongoClient().get_database("blight")
    response = db.users.update_one({"userid":userid}, {"$set": user_obj })
    return(get_user_info(userid)) 

# user_obj = {'lastSeen': '123'}
# print(update_user_info("virusman", user_obj))

def update_user_virion(userid, virion):
    db = MongoClient().get_database("blight")
    response = db.users.update_one({"userid":userid}, {"$set": {"balance":virion} })
    response = db.users.find_one({"userid":userid}, {"balance": 1, "_id": 0})
    return(response)

# print(update_user_virion("virusman", "5000"))


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]


def store_items_load():
    l = []
    db = MongoClient().get_database("blight")
    storeMinerItems = db.store.find({"type":"miner"}, { "item": 1, "_id": 0})
    storeMinerItems = (list(storeMinerItems))
    for itemName in storeMinerItems:
        for key, val in itemName.items():
            smallList=[]
            smallList.append(val)
            l.append(smallList)

    itemsJsonList = [{chunk[i][0] : "0"   for i in range(len(chunk))} 
              for chunk in chunks(l, 12)]

    return (itemsJsonList)
        