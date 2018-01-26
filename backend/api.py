from flask import Flask, request
app = Flask(__name__)

from . import authentication

@app.route("/api")
def hello():
    return "Hello GGJ2018!"


@app.route('/api/authenticate', methods=['POST'])
def add_message(uuid):

    token = request.headers["X-AUTH"] or None
    if token:
        authenticated = authentication.authenticate_token(token)
    else:
        content = request.json
        print(content)
        username=content["username"]
        password=content["password"]
        authenticated = authentication.authenticate(username, password)

    return authenticated



if __name__ == '__main__':
    app.run('0.0.0.0', 5000)

