from flask import render_template, jsonify, request

from app import app, session
from app.models import Location, Base, AlchemyEncoder, User
import json


@app.route("/")
def hello():

    users = session.query(User).all()

    return render_template('index.html', users=users)


@app.route("/fetch_data", methods=['POST'])
def fetch_data():
    print("Got new request")
    print(request.json)
    username = request.json["username"]
    print("username is: ", username)

    user = session.query(User).filter_by(username=username).first()
    print("User is: ", user)

    if user is None:
        if username != "all":
            raise Exception("No user found!")

    locations = session.query(Location)
    if username == "all":
        locations = locations.all()
    else:
        locations = locations.filter_by(user_id=user.id).all()

    return json.dumps(locations, cls=AlchemyEncoder)
