import requests
from pymongo import MongoClient
from time import sleep
import logging
logger = logging.getLogger("blight")

apikey = "AIzaSyDZEOKPfu1-yvYeSSuT8-cpDgnAKTtjKLk"
db = MongoClient().get_database("blight")

def parse_location(local):
    name = local["name"]
    lat = local["geometry"]["location"]["lat"]
    lng = local["geometry"]["location"]["lng"]
    icon = "https://assets.ifttt.com/images/channels/703096546/icons/on_color_large.png"

    retjson = {
        "name":name,
        "lat":lat,
        "lng":lng,
        "icon":icon,
        "virion": 0,
        "max": 100000000,
        "min": -100000000,
        "neutral_max":10000,
        "neutral_min":-10000,
        "team":"neutral",
        "inventoryItems":[],
        "degradeRate":5,
        "range":100,
        "max_inventory":9,
        "base_mod":0.5
    }
    return retjson


def find_places(location = '51.481581,-3.179090', radius=500):

    page_token = 'stupidtoken'

    logger.debug("location = " + location)
    while page_token:

        params = {'location': location, "radius": radius, "type": "points_of_interest", "key": apikey}
        if page_token != "stupidtoken":
            params["pagetoken"] = page_token

        resp = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json', params=params)
        logger.info("Querying google api for places.. \nRequest:" + resp.url)
        logger.debug(resp.status_code
                     )
        data = resp.json()["results"]
        try:
            page_token = resp.json()["next_page_token"]
        except KeyError:
            page_token = False
            pass

        logger.debug(page_token)
        for local in data:
            deets = parse_location(local)
            store_in_db(deets)

        sleep(2)


def store_in_db(local):

    out = db.landmarks.remove({"name":local["name"]})
    if out["n"]:
        logger.info("Removed " + local["name"])

    db.landmarks.insert(local)
    logger.info("Inserted " + local["name"] + " into landmarks collection")


if __name__ == '__main__':
    find_places()




