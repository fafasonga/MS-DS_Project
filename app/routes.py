from flask import render_template, jsonify, request

from app import app, session
from app.models import Location, Base, AlchemyEncoder, User
import json


@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == 'POST':
        print("Got new request")
        username = request.form["username"]
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
        locations = json.dumps(locations, cls=AlchemyEncoder)
    else:
        locations = ""
    users = session.query(User).all()

    return render_template("index.html", data=locations, users=users)


@app.route("/table")
def fill_table():
    locations = session.query(Location, User).join(User).add_columns(User.username, Location.id, Location.lat, Location.lan, Location.timestamp).all()
    return render_template('tables.html', data=locations)