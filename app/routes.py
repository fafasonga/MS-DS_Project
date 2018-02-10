from datetime import datetime
from flask import render_template, jsonify, request
from werkzeug.utils import redirect

from app import app, session
from app.models import Location, Base, AlchemyEncoder, User
import json

# This block is used to bind the Url to a specific request or action and allow the comminication
# between the server and the web application

# Routing for the main home page
@app.route("/", methods=["GET", "POST"])
def hello():
    count = 0
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
        print("Data length is: {}".format(len(locations)))
        count = len(locations)

        locations = json.dumps(locations, cls=AlchemyEncoder)
    else:
        locations = ""
    users = session.query(User).all()

    return render_template("index.html", data=locations, users=users, count=count)


# Routing for accessing the Database page
@app.route("/table")
def fill_table():
    locations = session.query(Location, User).join(User).add_columns(User.username, Location.id, Location.lat,
                                                                     Location.lan, Location.timestamp).all()
    return render_template('tables.html', data=locations)


# Routing for the page to add new data to the Database
@app.route("/add_location", methods=['POST', 'GET'])
def fill_db():
    if request.method == 'POST':
        lat = request.form['lat']
        lan = request.form['lan']
        timestamp = request.form['timestamp']
        user_id = request.form['user_id']
        print(timestamp)
        ts = datetime.strptime(timestamp, "%Y-%m-%d")
        location = Location(lat, lan, ts, user_id)
        session.add(location)
        session.flush()
        return redirect("/")
    else:
        users = session.query(User).all()
        return render_template('add_location.html', users=users)


# Routing for the page to delete data from the Database
@app.route("/remove_location", methods=["POST", "GET"])
def remove_location():
    if request.method == 'POST':
        location = request.form.getlist('location[]')
        print(location)

        session.query(Location).filter(Location.id.in_(location)).delete(synchronize_session='fetch')

        return redirect("/")
    else:
        locations = session.query(Location).all()
        return render_template("remove_location.html", locations=locations)


# Routing for the page to add new users to the Database
@app.route("/add_user", methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        user = User(username)
        session.add(user)
        session.flush()
        return redirect("/")
    else:
        return render_template("add_user.html")


# Routing for the page to delete users to the Database
@app.route("/remove_user", methods=["POST", "GET"])
def remove_user():
    if request.method == 'POST':
        user = request.form.getlist('user[]')
        print(user)

        session.query(User).filter(User.id.in_(user)).delete(synchronize_session='fetch')

        return redirect("/")
    else:
        users = session.query(User).all()
        return render_template("remove_user.html", users=users)
