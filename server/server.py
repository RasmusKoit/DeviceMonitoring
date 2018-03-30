import flask
from flask import request
from pprint import pprint
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///server.db'
db = SQLAlchemy(app)

def generateRandomApiKey():
    return secrets.token_urlsafe(80)

class ApiKeys(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    api_key = db.Column(db.String(80), unique=True, nullable=False, default=generateRandomApiKey)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/api", methods=["post"])
def monitoringDataReceiver():
    api_key = request.headers.get('api-key')
    if getApiKey(api_key):
        pprint(request.json)
        return "OK", 201
    else:
        request.data  # Emptys receive buffer data
        return "error", 403

def getApiKey(api_key):
    return ApiKeys.query.filter_by(api_key = api_key).first()


def createApiKey(name):
    api_key = ApiKeys(name = name)
    db.session.add(api_key)
    db.session.commit()
    return api_key

if __name__ == '__main__':
    app.run(debug=True)
