from pymongo import MongoClient
from backend.landmarks.landmark import Landmark
def get_landmarks():
    db = MongoClient().get_database("blight")
    landmarks = list(db.landmarks.find({}))
    return landmarks



ldm = Landmark("Carphone Warehouse")


