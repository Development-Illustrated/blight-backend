from flask import Flask, request
app = Flask(__name__)

from backend import authentication

@app.route("/api")
def hello():
    return "Hello GGJ2018!"


@app.route('/api/authenticate', methods=['POST'])
def add_message():
    try:
        token = request.headers["X-AUTH"]
    except KeyError:
        token = None

    if token:
        authenticated = authentication.authenticate_token(token)
    else:
        content = request.json
        print(content)
        username=content["username"]
        password=content["password"]
        authenticated = authentication.authenticate(username, password)

    if authenticated:
        return 200
    else:
        return "You suck, get lost!"



if __name__ == '__main__':
    app.run('0.0.0.0', 5000)

