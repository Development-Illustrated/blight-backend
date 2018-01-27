from flask import Flask, request, Response, jsonify
app = Flask(__name__)
import json
from bson import ObjectId
from backend import authentication
from backend.landmarks import landmark_manager
from backend.user import user_info

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
    if not authentication.authenticate_token(request):
        return Response("Unauthorised access", status=401)

    return Response(JSONEncoder().encode(landmark_manager.get_landmarks()), status=200, mimetype='application/json')


@app.route('/api/user/get', methods=['GET'])
def get_user_info():
    if not authentication.authenticate_token(request):
        return Response(status=401)

    return user_info.get_user_info()











if __name__ == '__main__':
    app.run('0.0.0.0', 5000)

