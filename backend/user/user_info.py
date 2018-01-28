from pymongo import MongoClient
import time

def get_user_info(userid):
    db = MongoClient().get_database("blight")
    userInfo = db.users.find_one({"userid":userid})
    return userInfo

# print(get_user_info("virusman"))

#TODO dynamincaly load inventory items from stores table
def create_user_info(userid, team):
    db = MongoClient().get_database("blight")
    userExists = db.users.find({"userid":userid}).count()
    print(userExists)
    if userExists:
        return(get_user_info(userid))
    else:
        print("Creating new user:")
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
            "minersInactiveInventory" : [
                {
                "miniMiner" : "0",
                "medMiner" : "0",
                "megaMiner": "0"
                }
            ],
            "minersActiveInventory" : [
                {
                "miniMiner" : "0",
                "medMiner" : "0",
                "megaMiner": "0"
                }
            ],
            "radius" : defRadius,
            "lastSeen" : lastSeen
        }
        response = db.users.insert(userInfo)
        return(get_user_info(userid)) 

# print(create_user_info('virusmansd2', "red"))

def update_user_info(userid, user_obj):
    db = MongoClient().get_database("blight")
    response = db.users.update_one({"userid":userid}, {"$set": user_obj })
    return(get_user_info(userid)) 

# user_obj = {'lastSeen': '123'}
# print(update_user_info("virusman", user_obj))
