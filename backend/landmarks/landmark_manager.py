from pymongo import MongoClient
from backend.landmarks.landmark import Landmark

def get_landmarks():
    db = MongoClient().get_database("blight")
    landmarks = list(db.landmarks.find({}))
    return landmarks

def manage():
    # loop each landmark
    #



ldm = Landmark("Carphone Warehouse")


