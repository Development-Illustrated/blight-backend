from pymongo import MongoClient
import numpy as np
import logging

class Player(object):

    def __init__(self, name):
        self.logger = logging.getLogger('blight')
        self.logger.info('Instantiating player object for' + str(name))

        self.db = MongoClient().get_database("blight")
        doc = self.db.user.find_one({"name": name})
        if not doc:
            self.logger.warning("Couldn't find player with name: " + str(name))
            return

        try:
            self.id = str(doc["id"])
            self.name = doc["username"]
            self.resources = doc["virionBal"]
            self.lat = doc["lat"]
            self.lng = doc["lng"]
            self.team = doc["team"]
            self.itemResourceRate = doc["minersActiveInventory.miniMiner"]
            self.itemContagion = doc["minersActiveInventory.medMiner"]
            self.itemContagion = doc["minersActiveInventory.megaMiner"]
            self.radius = doc["radius"]

        except KeyError:
            self.logger.warning("player: Couldn't find all the required keys!")
            return

    # plenty of things will not work but I will try to fix them
    # playerLocation = [x1, y1], x1 and y1 being their coordinates, 100 being metres away
    # boolean result
    def calcDist(x2, y2):
        if (float(x2) <= 100) or (float(y2) <= 100):
            dist = np.sqrt( (x2 - 0)**2 + (y2 - 0)**2) < 100
            print(dist)
            return dist

    # resource counter per second
    def playerResourceIncrease(resources, itemResourceRate):
        resources += itemResourceRate
        # figure out the second delay
        return resources

    # The effect they'll have on other players
    def calcPlayerResourcePressure(resources, itemContagion):
        if resources < 100000:
            pressure = 0.0000005 * resources * (1 + itemContagion)
            return pressure
        else:
            pressure = 0.05 * (1 + itemContagion)
            return pressure

    # for players with in dist, calculate the effect they have on the player
    def calcPlayerResourceEfficiency(itemImmunity):
    # both effects should sum the array of all nearby players respective pressures
        allyEffect = sum(["nearby allies"])
        enemyEffect = sum(["nearby enemies"])

        effectiveMod = (1 + allyEffect - enemyEffect) * (1 + itemImmunity)

        if -0.75 < effectiveMod < 1.75:
            return effectiveMod
        elif effectiveMod <= -0.75:
            effectiveMod = 1 - 0.75
            return effectiveMod
        elif effectiveMod >= 1.75:
            effectiveMod = 1.75
            return effectiveMod