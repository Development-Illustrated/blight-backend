from pymongo import MongoClient
import uuid

def authenticate_token(token):

    db = MongoClient()
    tokens = db.get_database("blight").get_collection("tokens")

    if tokens.find({"username":token}):
        return True
    else:
        return False

def authenticate(username, password):
    db = MongoClient()
    users = db.get_database("blight").get_collection("users")

    if users.find({{"username":username},{"password":password}}):
        token = uuid.uuid4().hex
        return token
    else:
        return False


