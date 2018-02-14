import datetime
import json

from sqlalchemy import Integer, Column, ForeignKey, DateTime, Float, String
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

Base = declarative_base()

# creating the template for our Database

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    if isinstance(data, datetime.datetime):
                        fields[field] = data.__str__()
                    else:
                        fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), index=True, unique=True)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return self.username


class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True)
    lat = Column(Float)
    lan = Column(Float)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, lat, lan, timestamp, user_id):
        self.lan = lan
        self.lat = lat
        self.timestamp = timestamp
        self.user_id = user_id

    def __repr__(self):
        return "ID: {}. lat: {}. lan: {}. Timestamp: {}".format(self.id, self.lat, self.lan, self.timestamp)
