from datetime import datetime
from sys import argv, exit
from app import session
from app.models import Location, User

ctr = 0

users = {"name": 0}
original_file = ""

try:
    original_file = argv[1]
except IndexError:
    print("Please, provide correct CSV file!")
    print("Example: 'python converter.py /path/to/file.csv'")
    exit(-1)

with open(original_file) as f:
    lines = f.readlines()
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
        except ValueError:
            continue
        user_id = users[data[0]]
        location = Location(data[1], data[2], ts, user_id)
        print(location)
        session.add(location)
        session.flush()
