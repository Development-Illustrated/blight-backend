from pymongo import MongoClient
import json

def get_store_catalogue():
    db = MongoClient().get_database("blight")
    store_cat = list(db.store.find())
    return store_cat
