from pymongo import MongoClient

def get_user_info():
    db = MongoClient.get_database("blight")
    user = db.users.find()
    return user


print(get_user_info())