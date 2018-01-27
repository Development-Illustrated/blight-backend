from flask import Flask, request, Response
app = Flask(__name__)

from backend import authentication
from backend.landmarks import landmark_manager
from backend.user import user_info
@app.route("/api")
def hello():
    return "Hello GsGJ2018!"


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
        return Response({"key":authenticated}, status=200, mimetype='application/json')
    else:
        return Response(status=401)


@app.route('/api/landmarks', methods=['GET'])
def get_landmarks():
    if not authentication.authenticate_token(request):
        return Response(status=401)

    return landmark_manager.get_landmarks()


@app.route('/api/user/get', methods=['GET'])
def get_user_info():
    if not authentication.authenticate_token(request):
        return Response(status=401)

    return user_info.get_user_info()











if __name__ == '__main__':
    app.run('0.0.0.0', 5000)

