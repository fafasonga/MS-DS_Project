from datetime import datetime

from app import session
from app.models import Location

counter = 0

original_file = "/Users/admin/myapp/users.csv"
with open(original_file) as f:
    for line in f.readlines()[1:]:
        line = line.strip()
        if line == "":
            pass

        data = line.split(";")

        if data[0] == 'name':
            pass
        ts = datetime.strptime(data[3] + " " + data[4], "%d/%m/%Y %H:%M:%S")
        user_id = 1 if data[0] == 'user 1' else 2
        print(ts)
        l = Location(data[1], data[2], ts, user_id)
        session.add(l)
        session.flush()