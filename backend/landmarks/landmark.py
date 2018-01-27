from pymongo import MongoClient
from backend.tools import geo_tools
import logging

# calculate the effect landmarks have on player
class Landmark(object):
    landmarkBaseMod = 0.5

    def __init__(self, name):

        self.logger = logging.getLogger('blight')
        self.logger.info('Instantiating landmark object for ' + str(name))

        self.db = MongoClient().get_database("blight")
        doc = self.db.landmarks.find_one({"name": name})
        if not doc:
            self.logger.warning("Couldn't find landmark with name: " +str(name))
            return

        try:
            self.id = str(doc["id"])
            self.name = name
            self.resources = doc["virion"]
            self.items = doc["inventoryItems"]
            self.team = doc["team"]
            self.range = doc["range"]

        except KeyError:
            self.logger.warning("landmark: Couldn't find all required keys!")
            return

    def addItem(self, item):
        self.items.append(item)

    def captureLandmark(self, resources):
        self.landmarkResources = resources


    def add_virion(self, quantity, user):

        # TODO check user is within range of the landmark before updating
        # if not geo_tools.within_range([123,123], [123,123],500):
        #     return False

        if user.resource < quantity:
            self.logger.warning("User's resource isn't sufficient for request.")
            return False

        new_quant = self.resources + quantity

        self.db.landmarks.update({ "_id":self.id },
        { "$set":
            {
            "virion": new_quant
            }
        })
        self.logger.info("Updated mongo with new quantity")

        return True

