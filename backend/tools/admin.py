from pymongo import MongoClient

# Setup logger
import logging
logger = logging.getLogger("blight")

def del_users():
    db = MongoClient().get_database("blight")
    db.users.delete_many({})
    return


