from threading import Event
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    data = db.Column(db.String(10000))
    img = db.Column(db.String(500))
    status = db.Column(db.Integer)
    tickets = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(5))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    dateofbirth = db.Column(db.String(10))
    country = db.Column(db.String(3))
    email = db.Column(db.String(150), unique=True)
    Events = db.relationship('Event')
