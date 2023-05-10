from flask_login import UserMixin
from sqlalchemy.sql import func

from website.static.db import db


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(150))
    description = db.Column(db.String(1000))
    category = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    max_participants = db.Column(db.Integer)
    location = db.Column(db.String(200))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    events = db.relationship('Event')
