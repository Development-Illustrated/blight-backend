from pymongo import MongoClient
from backend.landmarks.landmark import Landmark
import random
from pprint import pprint
from time import sleep

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

def auto_manage(sleep_time = 0):
    while True:
        manage()

        sleep(sleep_time)



# Function intended to be looped by seperate thread
# Monitors landmarks statuses and changes if required
def manage():

    logger.info("Landmark management started")
    # Loop each landmark
    for l in get_landmark_names():
        ldm = Landmark(l)

        # Update landmark faction if required
        ldm.check_faction()

    logger.info("Landmark management done")

    return


def simulate(loops = 10):

    for i in range(loops):
        logger.info("Start of simulation loop")
        logger.info("Adding random relative resources to each landmark")
        for l in get_landmark_names():
            ldm = Landmark(l)
            quant = random.randrange(-10000,10000)
            ldm.add_virion(quant)

        # Check for any faction changes
        logger.info("Altering faction state for each landmark")
        manage()
        logger.info("End of simulation loop\n")
        sleep(2)

