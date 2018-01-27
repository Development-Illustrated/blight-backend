from pymongo import MongoClient

def get_landmarks():
    db = MongoClient().get_database("blight")
    landmarks = list(db.landmarks.find({}))
    return landmarks


