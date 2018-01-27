from pymongo import MongoClient
from backend.landmarks.landmark import Landmark
import random
from pprint import pprint
# Setup logger
from backend.tools import log
logger = log.setup_custom_logger('blight')

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


    for i in range(5):
        # Loop each landmark
        for l in get_landmark_names():
            logger.info("Checking landmark: "+str(l))


            ldm = Landmark(l)
            choice = random.choice([-5000, 5000])
            ldm.add_virion(choice)
            logger.info(l + " has changed by " + str(choice))
            ldm.check_faction()



    return



print("starting")
manage()
print("done")

