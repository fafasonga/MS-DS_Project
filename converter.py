from datetime import datetime

from app import session
from app.models import Location

ctr = 0

users = {}

original_file = "/Users/admin/myapp/users.csv"
with open(original_file) as f:
    for line in f.readlines()[1:]:
        line = line.strip()
        if line == "":
            pass

        data = line.split(";")

        if data[0] == 'name':
            pass

        if data[0] not in users:
            ctr += 1
            users[data[0]] = ctr

        ts = datetime.strptime(data[3] + " " + data[4], "%d/%m/%Y %H:%M:%S")
        user_id = users[data[0]]
        location = Location(data[1], data[2], ts, user_id)
        print(location)
        session.add(location)
        session.flush()
