from flask import Flask, request, Response, jsonify
import json
from bson import ObjectId

# Setup logger
from backend.tools import log
logger = log.setup_custom_logger('blight')
logger.debug('Initialising server')
logger.info('Initialising server')



from backend import authentication
from backend.landmarks import landmark_manager
from backend.landmarks.landmark import Landmark
from backend.landmarks import google_places
from backend.user import user_info


app = Flask(__name__)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)



@app.route("/api")
def hello():
    return "Hello GGJ2018!"


@app.route('/api/authenticate', methods=['POST'])
def authenticate():

    authenticated = authentication.authenticate_token(request)
    if authenticated:
       return Response(status="200")

    else:
        content = request.json
        print(content)
        if content:
            username=content["username"]
            password=content["password"]
            token = authentication.authenticate(username, password)

        else:
            return "No content, send me something fool!"

    if token:
        return Response(json.dumps({"key":token}), status=200, mimetype='application/json')
    else:
        return Response(status=401)


@app.route('/api/landmarks', methods=['GET'])
def get_landmarks():
    # if not authentication.authenticate_token(request):
    #     return Response("Unauthorised access", status=401)

    return Response(JSONEncoder().encode(landmark_manager.get_landmarks()), status=200, mimetype='application/json')



@app.route('/api/landmarks/refreshdb', methods=['GET'])
def refresh_landmarks():
    # if not authentication.authenticate_token(request):
    #     return Response("Unauthorised access", status=401)

    google_places.find_places()
    return Response(status=200)



@app.route('/api/landmarks/add_virion', methods=['PUT'])
def landmarks_add_virion():
    # if not authentication.authenticate_token(request):
    #     return Response("Unauthorised access", status=401)

    content = request.json
    if content:
        name = content["name"]
        quantity = content["quantity"]

    ldm = Landmark(name)

    return Response(JSONEncoder().encode(landmark_manager.get_landmarks()), status=200, mimetype='application/json')


#GET requests return JSON object containing user info
#POST requests creates a new entry for the new user in the db
@app.route('/api/user', methods=["GET","POST"])
def user():
    error = ''
    try:
	
        if request.method == "POST":
            userid = request.headers["userid"]
            content = request.json
            if userid and content:
                team=content["team"]
                response = user_info.create_user_info(userid, team)
            return str(response)

        if request.method == "GET":
            userid = request.headers["userid"]
            if userid:
                info = user_info.get_user_info(userid)
                return str(info)
            else:
                return "No userid provided, send me thats userid!"

    except Exception as e:
        return "Error! Unable to perform /api/user request"  

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
            return str(response)

    except Exception as e:
        return "Error! Unable to perform /api/user/update request" 

if __name__ == '__main__':

    app.run('0.0.0.0', 5000)

