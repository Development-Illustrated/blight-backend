import requests
from pymongo import MongoClient

apikey = "AIzaSyDZEOKPfu1-yvYeSSuT8-cpDgnAKTtjKLk"
db = MongoClient().get_database("blight")

def parse_location(local):
    name = local["name"]
    lat = str(local["geometry"]["location"]["lat"])
    lng = str(local["geometry"]["location"]["lng"])
    icon = local["icon"]

    retjson = {
        "name":name,
        "lat":lat,
        "lng":lng,
        "icon":icon,
        "ownershipTeam":None,
        "inventoryItems":[],
        "scheme": "",
        "status":"",
        "degradeRate":5

    }
    return retjson


def find_places(location = '51.481581,-3.179090', radius=500):
    params = {'location': location, "radius": radius, "type": "points_of_interest", "key": apikey}
    resp = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json', params=params)
    print("Querying google api for places.. \nRequest:" + resp.url)

    data = resp.json()["results"]

    for local in data:
        deets = parse_location(local)
        store_in_db(deets)




def store_in_db(local):

    out = db.landmarks.remove({"name":local["name"]})
    if out["n"]:
        print("Removed " + local["name"])

    db.landmarks.insert(local)
    print("Inserted " + local["name"] + " into landmarks collection")






