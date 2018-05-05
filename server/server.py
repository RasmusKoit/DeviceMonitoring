import flask
from flask import request
from pprint import pprint
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets
import statsd


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///server.db'
app.config['SQLALCHEMY_BINDS'] = {
    'key':  'sqlite:///unknown.db'
}
db = SQLAlchemy(app)
client = statsd.StatsClient('172.20.1.1')


def generateRandomApiKey():
    return secrets.token_urlsafe(80)


class LogRequest(db.Model):

    __bind_key__ = 'key'
    key = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)


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
        data = request.get_json(force=True)
        for key, value in data.items():
            for subKey, subValue in value.items():
                print(key, subKey, subValue)
                client.gauge("%s %s" %(key, subKey), subValue)
        return "OK", 201

    else:
        #Handle for keys that are added to unauth list
        if (LogRequest.query.filter_by(key = api_key).first()):

            return "Unauthorized", 401
        else:
            addApiKey(api_key)
            return "Unauthorized", 401


def getApiKey(api_key):
    return ApiKeys.query.filter_by(api_key = api_key).first()

def addApiKey(api_key):
    key = LogRequest(key=api_key)
    db.session.add(key)
    db.session.commit()


def createApiKey(name):
    api_key = ApiKeys(name = name)
    db.session.add(api_key)
    db.session.commit()
    return api_key



if __name__ == '__main__':
    app.run(debug=True)
