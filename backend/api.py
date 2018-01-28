import json
from bson import ObjectId
from flask import Flask, request, Response

from backend.tools import log
logger = log.setup_custom_logger('blight')
logger.info('Initialising server')

from backend.landmarks import landmark_manager
from backend.landmarks.landmark import Landmark
from backend.landmarks import google_places
from backend.user import user_info
from backend.store import store_engine

app = Flask(__name__)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route("/api")
def hello():
    return "Hello GGJ2018!"


@app.route('/api/landmarks', methods=['GET'])
def get_landmarks():
    # if not authentication.authenticate_token(request):
    #     return Response("Unauthorised access", status=401)

    return Response(JSONEncoder().encode(landmark_manager.get_landmarks()), status=200, mimetype='application/json')


@app.route('/api/landmarks/add_landmarks', methods=['POST'])
def refresh_landmarks():
    # if not authentication.authenticate_token(request):
    #     return Response("Unauthorised access", status=401)

    content = request.json
    if not content:
        return Response("Send me some coords yo", status=400)

    lat = content["lat"]
    lng = content["lng"]


    location = str(lat) + ', ' + str(lng)
    logger.debug("location: " +location)

    google_places.find_places(location)

    return Response(JSONEncoder().encode(landmark_manager.get_landmarks()), status=200, mimetype='application/json')

@app.route('/api/landmarks/search', methods=['GET'])
def search_landmarks():
    # if not authentication.authenticate_token(request):
    #     return Response("Unauthorised access", status=401)

    content = request.json
    if not content:
        return Response("Send me some coords yo", status=400)

    name = content["name"]
    resp = landmark_manager.get_landmarks(name)
    if resp:
        return Response(JSONEncoder().encode(resp), status=200, mimetype='application/json')
    else:
        return Response("Couldn't find required info, sorry", status=400, mimetype='application/json')


@app.route('/api/landmarks/add_virion', methods=['POST'])
def landmarks_add_virion():
    # if not authentication.authenticate_token(request):
    #     return Response("Unauthorised access", status=401)

    content = request.json
    if not content:
        return Response('Send me some stuff', status=400)

    name = content["name"]
    quantity = content["quantity"]
    landmark = content["landmark"]

    ldm = Landmark(landmark)
    ldm.add_virion(quantity)


    return Response(JSONEncoder().encode(landmark_manager.get_landmarks()), status=200, mimetype='application/json')


#GET requests return JSON object containing user info
#POST requests creates a new entry for the new user in the db
@app.route('/api/user', methods=["GET","POST"])
def user():

    if request.method == "POST":
        userid = request.headers["userid"]
        content = request.json
        if userid and content:
            team=content["team"]
            response = user_info.create_user_info(userid, team)
            return Response(JSONEncoder().encode(response), status=200, mimetype='application/json')
        else:
            return Response("get me some more shiz", status=401)

    if request.method == "GET":
        userid = request.headers["userid"]
        if userid:
            info = user_info.get_user_info(userid)
            if info:
                return Response(JSONEncoder().encode(info), status=200, mimetype='application/json')
            else:
                return Response("User doesn't exist", status=401)
        else:
            return Response("No user id provided", status=400)


#Updates given user's info
@app.route('/api/user/update', methods=["POST"])
def updateUser():
    error = ''
    try:
        userid = request.headers["userid"]
        content = request.json
        print(userid)
        print(content)
        if userid and content:
            print("Updating user info")
            response = user_info.update_user_info(userid, content)
            return Response(JSONEncoder().encode(response), status=200, mimetype='application/json')

    except Exception as e:
        return "Error! Unable to perform /api/user/update request"

#Update given user's virion(balance)
@app.route('/api/user/update/virion', methods=["POST"])
def updateVirion():
    error = ''
    try:
        userid = request.headers["userid"]
        content = request.json
        virion = content["balance"]
        if userid and content:
            print("Updating user virion balance ...")
            response = user_info.update_user_virion(userid, virion)
            return Response(JSONEncoder().encode(response), status=200, mimetype='application/json')

    except Exception as e:
        return "Error! Unable to perform /api/user/update/virion request"


#Updates given user's info
@app.route('/api/store', methods=["GET"])
def getCatalogue():
    error = ''
    try:
        response = store_engine.get_store_catalogue()
        return Response(JSONEncoder().encode(response), status=200, mimetype='application/json')

    except Exception as e:
        return "Error! Unable to perform /api/store request"


# Simulates users spending resource
@app.route('/api/simulate', methods=["POST"])
def simulate():

    loops = int(request.args.get("loops"))
    landmark_manager.simulate(loops)

    return Response(status=200)


if __name__ == '__main__':

    app.run('0.0.0.0', 5000, use_reloader=False)