import json

from flask import render_template, request, flash
from werkzeug.utils import redirect

from app import app, session
from app.forms import LocationForm
from app.models import Location, AlchemyEncoder, User
from app.utils import upload_csv


# This block is used to bind the Url to a specific request or action and allow the communication
# between the server and the web application


# Routing for the main home page
@app.route("/", methods=["GET", "POST"])
def home():
    count = 0
    if request.method == 'POST':
        print("Got new request")
        username = request.form.getlist('username')
        print("username is: ", username)

        user = session.query(User).filter(User.username.in_(username)).all()
        print("User is: ", user)

        if user is None:
            if username != "all":
                raise Exception("No user found!")

        locations = session.query(Location)
        if username == "all":
            locations = locations.all()
        else:
            locations = locations.filter(Location.user_id.in_([u.id for u in user])).all()
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
    return render_template("tables.html", data=locations)


# Routing for the page to add new data to the Database
@app.route("/add_location", methods=['POST', 'GET'])
def fill_db():
    form = LocationForm()
    print(form.user_id.data)

    if form.validate_on_submit():
        location = Location(lat=form.lat.data, lan=form.lan.data, timestamp=form.timestamp.data, user_id=form.user_id.data)
        session.add(location)
        session.flush()
        return redirect("/")
    else:
        users = session.query(User).all()
        return render_template("add_location.html", users=users, form=form)


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


# Routing for the page to delete users from the Database
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


# Uploading New CSV files from Computer directories
@app.route("/upload_csv", methods=["POST", "GET"])
def upload_data():
    if request.method == 'POST':
        # session.begin()
        # session.query(Location).delete()
        # session.query(User).delete()
        # session.commit()
        file = request.files.getlist('file[]')
        print(file)
        result = upload_csv(file)
        if result != "OK":
            flash(result)
        else:
            flash("File successfully uploaded!")
            return redirect("/table")
    return render_template("upload_csv.html")


# Clearing the Existing Database
@app.route("/delete_database", methods=["GET", "POST"])
def delete_database():
    if request.method == 'POST':
        session.begin()
        session.query(Location).delete()
        session.query(User).delete()
        session.commit()
        return redirect("/table")
    return render_template("delete_database.html")


general_template = '{"type": "FeatureCollection", "features": [%s]}'
template = '{"geometry": {"type": "LineString", "coordinates": [[%s, %s], [%s, %s]]}, ' \
           '"type": "Feature", "properties": {"style": {"color": "red", "weight": 3}, "times": ["%s", "%s"]}}'


# # Function to display Animations to the map
# def group(lst, n):
#     return zip(*[lst[i::n] for i in range(n)])
#
#
# @app.route("/line_draw", methods=["GET", "POST"])
# def line_draw():
#     geometries = []
#     locations = session.query(Location).all()
#     locations = group(locations, 2)
#     for location in locations:
#         l1, l2 = location
#         geometries.append(template % (l1.lan, l1.lat, l2.lan, l2.lat, str(l1.timestamp.strftime("%Y-%m-%dT%H:%M:%S")),
#                                       str(l2.timestamp.strftime("%Y-%m-%dT%H:%M:%S"))))
#
#     return render_template('line_draw.html', asdf=json.loads(general_template % ", \n".join(geometries)))
