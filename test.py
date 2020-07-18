import flask
from flask_cors import CORS, cross_origin

app = flask.Flask(__name__)
@app.route("/", methods=["GET"])
@cross_origin()
def home():
    return "Hello World" 

@app.route("/image/<id>")
@cross_origin()
def getImage(id):
    return "Hello {}".format(id)
