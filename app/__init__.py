from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os

from app.models import User, Base
from app.settings import DATABASE, DEBUG

engine = create_engine(DATABASE, convert_unicode=True)
engine.echo = DEBUG


engine.connect()

db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))
session = db_session()
Base.metadata.create_all(engine)


template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),  'templates')
static_foler = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_foler)
app.config['SECRET_KEY'] = settings.SECRET_KEY

from app import routes, models
