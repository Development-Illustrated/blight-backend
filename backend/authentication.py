from pymongo import MongoClient
import uuid
import time
from pprint import pprint

def authenticate_token(token):

    db = MongoClient().get_database("blight")
    token = db.tokens.find({"token":token}).count()

    if token:
        return "200"
    else:
        return False


def authenticate(username, password):
    db = MongoClient().get_database("blight")

    out = db.tokens.remove({"username":username})
    print("Users deleted: " + str(out["n"]))
    user = db.users.find({"$and":[{"username": username}, {"password": password}]}).count()
    if user:
        token = uuid.uuid4().hex    # Generate token
        timeout = int(time.time()+60*60) # Add one hour to current time
        pprint({"username":username,"token":token, "expireOnTs":timeout})
        db.tokens.insert({"username":username,"token":token, "expireOnTs":timeout})
        return token
    else:
        return False


