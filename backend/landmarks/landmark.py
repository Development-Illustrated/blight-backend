from pymongo import MongoClient
from backend.tools import geo_tools

# calculate the effect landmarks have on player
class Landmark(object):
    landmarkBaseMod = 0.5

    def __init__(self, name):
        self.db = MongoClient().get_database("blight")
        doc = self.db.landmarks.find_one({"name": name})
        if not doc:
            print("Couldn't find landmark with name: " +str(name))
            return

        try:
            self.name = name
            self.resources = doc["virion"]
            self.items = doc["inventoryItems"]
            self.team = doc["team"]
            self.range = doc["range"]

        except KeyError:
            print("landmark: Couldn't find all required keys!")
            return

    def addItem(self, item):
        self.items.append(item)

    def captureLandmark(self, resources):
        self.landmarkResources = resources


    def add_virion(self, quantity, user):

        if not geo_tools.within_range([123,123], [123,123],500):
            return False

        doc = self.db.landmarks.find_one({"name":self.name})
        id = str(doc["_id"])
        curr_quant = int(doc["virion"])
        new_quant = curr_quant + quantity

        self.db.landmarks.update({ "_id":id },
       { "$set":
          {
            "virion": new_quant
              }
       })






