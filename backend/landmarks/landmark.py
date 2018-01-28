from pymongo import MongoClient
from backend.tools import geo_tools
import logging
logger = logging.getLogger("blight")

# calculate the effect landmarks have on player
class Landmark(object):

    def __init__(self, name):

        self.logger = logging.getLogger('blight')

        self.db = MongoClient().get_database("blight")
        doc = self.db.landmarks.find_one({"name": name})
        if not doc:
            self.logger.warning("Couldn't find landmark with name: " +str(name))
            return

        try:
            self.id = str(doc["_id"])
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

        except KeyError as e:
            self.logger.critical("landmark: Couldn't find all required keys!", e)


    def get_settings(self):
        with open('backend/landmarks/stats.ini', 'r') as f:
            lines = f.readlines()
            settings = {}
            for l in lines:
                l = l.strip()
                l = l.strip('\n')
                settings[l.split('=')[0]] = l.split("=")[1]

        return settings

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

        settings = self.get_settings()
        # logger.debug("NAME:"+str(self.name))
        # logger.debug("NMIN:"+str(self.nmin))
        # logger.debug("NMAX:"+str(self.nmax))
        # logger.debug("MIN:"+str(self.min))
        # logger.debug("MAX:"+str(self.max))
        # logger.debug("resources:"+str(self.resources))

        if self.resources in range(int(self.nmax), int(self.max)):
            new_team = 'virus'
            new_image = settings["virusimage"]
        elif self.resources in range(int(self.min), int(self.nmin)):
            new_team = 'bacteria'
            new_image = settings["bacteriaimage"]
        else:
            new_team = 'neutral'
            new_image = settings["neutralimage"]

        if self.team != new_team:
            self.logger.debug(self.name + " has changed teams from  " +self.team +" to  " + new_team)
            self.team = new_team
            self.db.landmarks.update_one({"name":self.name},{"$set": {"team":self.team, "icon":new_image}})

        return

    def add_virion(self, quantity):

        # TODO check user is within range of the landmark before updating
        # if not geo_tools.within_range([123,123], [123,123],500):
        #     return False

        # if user.resource < quantity:
        #     self.logger.warning("User's resource isn't sufficient for request.")
        #     return False

        new_quant = self.resources + quantity

        self.db.landmarks.update_one({ "name":self.name },
        { "$set":
            {
            "virion": new_quant
            }
        })

        return True
