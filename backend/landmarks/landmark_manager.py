from pymongo import MongoClient
from backend.landmarks.landmark import Landmark
import logging
logger = logging.getLogger('blight')

def get_landmarks():
    db = MongoClient().get_database("blight")
    landmarks = list(db.landmarks.find({}))
    logger.info("Returning landmarks from mongo")
    return landmarks

def get_landmark_names():
    db = MongoClient().get_database("blight")
    x = list(db.landmarks.find({},{"name":1}))
    landmarks = []
    for i in x:
        landmarks.append(i["name"])

    return landmarks

def manage():
    # check landmark factions
    for l in get_landmark_names():
        logger.info("Checking landmark: "+str(l))
        ldm = Landmark(l)
        ldm.check_faction()

    return



print("starting")
manage()
print("done")

