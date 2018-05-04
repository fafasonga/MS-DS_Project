from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.fields import FloatField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import DataRequired

from app import session, User, settings


def get_users():
    users = session.query(User).all()
    return [(user.id, user.username) for user in users]


class LocationForm(FlaskForm):
    lat = FloatField('Latitude', validators=[DataRequired()], render_kw={"placeholder": "46.22222"})
    lan = FloatField('Longitude', validators=[DataRequired()], render_kw={"placeholder": "11.2222"})
    timestamp = DateTimeField('Timestamp', validators=[DataRequired()], format=settings.DATETIME_FORMAT, render_kw={"placeholder": "30/12/2016 23:59:01"})
    user_id = SelectField('User', choices=get_users(), coerce=int)
    submit = SubmitField('Submit')
