from pymongo import MongoClient

# calculate the effect landmarks have on player
class Landmark(object):
    landmarkBaseMod = 0.5

    def __init__(self, name):
        db = MongoClient().get_database("blight")
        doc = db.landmarks.find_one({"name": name})
        if not doc:
            print("Couldn't find landmark with name: " +str(name))
            return

        try:
            self.name = name
            self.landmarkResources = doc["virion"]
            self.landmarkItems = doc["inventoryItems"]
            self.landmarkTeam = doc["team"]
        except KeyError:
            print("landmark: Couldn't find all required keys!")

    def addItem(self, item):
        self.landmarkItems.append(item)

    def captureLandmark(self, resources):
        self.landmarkResources = resources


    def add_virion(self, quantity):
        if self.within_range([123,123]):




