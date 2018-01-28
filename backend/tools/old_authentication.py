from pymongo import MongoClient
import uuid
import time
from pprint import pprint

# @app.route('/api/authenticate', methods=['POST'])
# def authenticate():
#
#     authenticated = old_authentication.authenticate_token(request)
#     if authenticated:
#        return Response(status="200")
#
#     else:
#         content = request.json
#         print(content)
#         if content:
#             username=content["username"]
#             password=content["password"]
#             token = old_authentication.authenticate(username, password)
#
#         else:
#             return "No content, send me something fool!"
#
#     if token:
#         return Response(json.dumps({"key":token}), status=200, mimetype='application/json')
#     else:
#         return Response(status=401)


def authenticate_token(req):

    authenticated = None

    try:
        token = req.headers["X-AUTH"]
    except KeyError:
        token = None
        return False

    db = MongoClient().get_database("blight")
    token = db.tokens.find({"token":token}).count()

    if token:
        return token
    else:
        return False


def authenticate(username, password):
    db = MongoClient().get_database("blight")

    out = db.tokens.remove({"username":username})
    print("Users deleted: " + str(out["n"]))
    user = db.users.find({"$and":[{"username": username}, {"password": password}]}).count()
    if user:
        token = uuid.uuid4().hex    # Generate token
        timeout = int(time.time()+60*60) # Add one hour to current time
        pprint({"username":username,"token":token, "expireOnTs":timeout})
        db.tokens.insert({"username":username,"token":token, "expireOnTs":timeout})
        return token
    else:
        return False


