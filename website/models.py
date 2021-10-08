from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    data = db.Column(db.String(10000))
    img = db.Column(db.String(500), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    tickets = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(10))
    ticketcost = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    Comment = db.relationship('Comment')
    Purchase = db.relationship('Purchase')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(5), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    dateofbirth = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(3), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phn = db.Column(db.String(10))
    Events = db.relationship('Event')
    Comments = db.relationship('Comment')
    Purchase = db.relationship('Purchase')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    data = db.Column(db.String(10000), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    notickets = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    purchasedate = db.Column(db.DateTime(timezone=False), default=func.now())