from pymongo import MongoClient
from backend.landmarks.landmark import Landmark
import random
from pprint import pprint
# Setup logger
import logging
logger = logging.getLogger("blight")

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
        try:
            landmarks.append(i["name"])
        except KeyError as e:
            print("KEY ERRROR:" + str(e))

    return landmarks

def manage():

    # Loop each landmark
    for l in get_landmark_names():
        ldm = Landmark(l)

        # Update landmark faction if required
        ldm.check_faction()

    return


