from flask import Flask, request
app = Flask(__name__)

@app.route("/api")
def hello():
    return "Hello GGJ2018!"


@app.route('/api/authenticate', methods=['GET', 'POST'])
def add_message(uuid):
    content = request.get_json(silent=True)
    print(content)
    return uuid


if __name__ == '__main__':
    app.run('172.31.13.62', 5000)

