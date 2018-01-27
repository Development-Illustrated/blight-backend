from pymongo import MongoClient
from backend.tools import geo_tools
import logging

# calculate the effect landmarks have on player
class Landmark(object):

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
            self.max = doc["max"]
            self.min = doc["min"]
            self.nmax = doc["neutral_max"]
            self.nmin = doc["neutral_min"]
            self.items = doc["inventoryItems"]
            self.max_items = doc["max_inventory"]
            self.team = doc["team"]
            self.range = doc["range"]

        except KeyError:
            self.logger.critical("landmark: Couldn't find all required keys!")


    def add_item(self, item, user):

        # TODO Check user is within range of the landmark

        if item not in user.items:
            self.logger.warning("User doesnt have the item the want to transfer.")
            return False

        if len(self.items) < self.max_items:
            self.logger.warning("Landmark doesn't have room for more items")
            return False

        self.items.append(item)
        self.logger.info("Item added to landmark inventory")

    def check_faction(self):
        old_team = self.team
        if self.resources in range(self.nmax, self.max):
            self.team = 'virus'
        elif self.resources in range(self.nmin, self.min):
            self.team = 'bacteria'
        else:
            self.team = 'neutral'

        if self.team is not old_team:
            self.logger.info(self.name + " has changed teams to  " + self.team)
        return

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

        # TODO if neutral
            # Change faction
        return True




