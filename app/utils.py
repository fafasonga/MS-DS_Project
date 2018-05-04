from datetime import datetime

from werkzeug.datastructures import FileStorage

from app import session
from app.models import Location, User

# Loading dataset to the Database from an external source

users = {"name": 0}


def check_csv(file):
    return "OK"


def upload_csv(files):

    if not isinstance(files, list):
        files = [files]

    for f in files:
        result = check_csv(f)
        if not isinstance(f, FileStorage):
            f = open(f)
        if result != "OK":
            return result
        global users
        users = dict(session.query(User).with_entities(User.username, User.id).all())
        ctr = users.get(max(users, key=users.get, default=0), 0)
        lines = f.readlines()
        lines = [l.decode('utf-8') for l in lines]
        for line in lines:
            line = line.strip()
            if line == "":
                pass

            data = line.split(";")

            if data[0].strip().lower() == 'name':
                continue

            if data[0].strip() not in users:
                ctr += 1
                users[data[0]] = ctr
                user = User(data[0])
                session.add(user)
            try:
                # print(data)
                # print("date: {}, time: {}".format(data[3], data[4]))
                ts = datetime.strptime(data[3] + " " + data[4], "%d/%m/%Y %H:%M:%S")
                # print("Timestamp is :", ts)
            except ValueError:
                continue
            user_id = users[data[0]]
            # print(data[0], users[data[0]])
            location = Location(data[1], data[2], ts, user_id)
            # print(location)
            session.add(location)
            session.flush()

        f.close()
    return "OK"
