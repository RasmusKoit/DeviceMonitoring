import flask
from flask import request
from pprint import pprint
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt, JWTManager)
import uuid
import hashlib
import json
import statsd
import settings

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_BINDS'] = {
    'key': settings.SQLALCHEMY_UNKNOWN_HUBS,
    'userAuthDB': settings.SQLALCHEMY_USER_DB
}
app.config['JWT_SECRET_KEY'] = settings.JWT_SECRET_KEY
jwt = JWTManager(app)

db = SQLAlchemy(app)
client = statsd.StatsClient(settings.STATSD_CLIENT_IP)


class user_auth(db.Model):
    __bind_key__ = 'userAuthDB'
    email = db.Column(db.String(80), primary_key=True, unique=True)
    passwordHash = db.Column(db.String(255))


class LogRequest(db.Model):
    __bind_key__ = 'key'
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    key = db.Column(db.String(80), unique=True, nullable=False)



class ApiKeys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    api_key = db.Column(db.String(80), unique=True, nullable=False)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/api/data", methods=["post"])
def monitoringDataReceiver():
    api_key = request.headers.get('api-key')
    print(getApiKey(api_key))
    if getApiKey(api_key):
        data = request.get_json(force=True)
        for key, value in data.items():
            for subKey, subValue in value.items():
                print(key, subKey, subValue)
                client.gauge("%s %s" % (key, subKey), subValue)
        return "OK", 201

    else:
        # Handle for keys that are added to unauth list
        if (LogRequest.query.filter_by(key=api_key).first()):

            return "Unauthorized", 401
        else:
            addApiKey(api_key)
            return "Unauthorized", 401


@app.route("/api/auth", methods=["post"])
def userLoggingIn():
    data = request.get_json(force=True)
    response = {}
    user = {
        "email": (data["credentials"]["email"]),
        "password": (data["credentials"]["password"])
    }
    if (checkUser(user)):
        response["user"] = {}
        response["user"]["email"] = user["email"]
        response["user"]["token"] = create_access_token(identity=user["email"])
        response = json.dumps(response)
        return response, 200
    else:
        response["errors"] = {}
        response["errors"]["global"] = "Invalid credentials"
        response = json.dumps(response)
        return response, 400


@app.route("/api/auth/hub", methods=["get"])
def listUnauthHubs():
    db.create_all()
    hub_key = request.args.get('q')
    unknownHubs = LogRequest.query.filter(LogRequest.key.contains(hub_key)).all()
    response = {
        "hubs": []
    }
    for hub in unknownHubs:
        response["hubs"].append({
            "key": hub.key,
            "id": hub.id
        })
    pprint(response)
    return json.dumps(response), 200



# check hashed password with password from credentials
def checkUser(user):
    dbUser = user_auth.query.filter_by(email=user["email"]).first()
    if dbUser is None:
        return False
    else:
        return check_password(dbUser.passwordHash, user["password"])


def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


def getApiKey(api_key):
    return ApiKeys.query.filter_by(api_key=api_key).first()


def addApiKey(api_key):
    key = LogRequest(key=api_key)
    db.session.add(key)
    db.session.commit()


def createApiKey(name):
    api_key = ApiKeys(name=name)
    db.session.add(api_key)
    db.session.commit()
    return api_key


if __name__ == '__main__':
    app.run(debug=True)
