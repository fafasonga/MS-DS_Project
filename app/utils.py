from datetime import datetime

from werkzeug.datastructures import FileStorage

from app import session
from app.models import Location, User

# Loading dataset to the Database from an external source


users = {"name": 0}


def check_csv(file):
    return "OK"


def upload_csv(f):
    result = check_csv(f)
    if not isinstance(f, FileStorage):
        f = open(f)
    if result != "OK":
        return result
    ctr = 0
    lines = f.readlines()
    lines = [l.decode('utf-8') for l in lines]
    print(lines)
    for line in lines:
        line = line.strip()
        if line == "":
            pass

        data = line.split(";")

        if data[0].strip() not in users:
            ctr += 1
            users[data[0]] = ctr
            user = User(data[0])
            session.add(user)
        try:
            ts = datetime.strptime(data[3] + " " + data[4], "%d/%m/%Y %H:%M:%S")
            print("Timestamp is :", ts)
        except ValueError:
            continue
        user_id = users[data[0]]
        location = Location(data[1], data[2], ts, user_id)
        print(location)
        session.add(location)
        session.flush()

    f.close()
    return "OK"
