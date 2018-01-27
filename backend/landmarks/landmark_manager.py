from pymongo import MongoClient
from backend.landmarks.landmark import Landmark
import logging
logger = logging.getLogger('blight')

def get_landmarks():
    db = MongoClient().get_database("blight")
    landmarks = list(db.landmarks.find({}))
    logger.info("Returning landmarks from mongo")
    return landmarks

def manage():
    # loop each landmark
    while True:





ldm = Landmark("Carphone Warehouse")


