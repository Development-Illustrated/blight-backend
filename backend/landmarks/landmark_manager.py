from pymongo import MongoClient

def get_landmarks():
    db = MongoClient.get_database("blight")
    landmarks = db.landmarks.find()
    return landmarks


print(get_landmarks())