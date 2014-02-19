# -*- coding: utf-8 -*-
import datetime as dt

from flask.ext.login import UserMixin

from autoposter.database import db, CRUDMixin
from autoposter.extensions import bcrypt


class User(UserMixin, CRUDMixin,  db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)  # The hashed password
    created_at = db.Column(db.DateTime(), nullable=False)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    active = db.Column(db.Boolean())
    is_admin = db.Column(db.Boolean())
    posts = db.relationship("Post", backref="user")

    def __init__(self, username=None, email=None, password=None,
                 first_name=None, last_name=None,
                 active=False, is_admin=False):
        self.username = username
        self.email = email
        if password:
            self.set_password(password)
        self.active = active
        self.is_admin = is_admin
        self.created_at = dt.datetime.utcnow()
        self.first_name = first_name
        self.last_name = last_name

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def __repr__(self):
        return '<User "{username}">'.format(username=self.username)


class Post(CRUDMixin, db.Model):

    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    subreddit = db.Column(db.String(20), nullable=False)
    body = db.Column(db.String(10000), nullable=True)
    days = db.relationship("DaysOfWeek", backref="post", uselist=False)
    distinguish = db.Column(db.Boolean)
    sticky = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    scheduled_hour = db.Column(db.Integer)
    scheduled_minute = db.Column(db.Integer)
    next_fire = db.Column(db.DateTime)

    def __init__(self, title="", subreddit="", body="", days=[False] * 7,
                 distinguish=False, sticky=False, scheduled_hour=0, scheduled_minute=0):
        self.title = title
        self.subreddit = subreddit
        self.body = body
        self.days = DaysOfWeek(days)
        self.days.save()
        self.distinguish = distinguish


class DaysOfWeek(CRUDMixin, db.Model):

    __tablename__ = 'days'
    id = db.Column(db.Integer, primary_key=True)
    monday = db.Column(db.Boolean)
    tuesday = db.Column(db.Boolean)
    wednesday = db.Column(db.Boolean)
    thursday = db.Column(db.Boolean)
    friday = db.Column(db.Boolean)
    saturday = db.Column(db.Boolean)
    sunday = db.Column(db.Boolean)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __init__(self, days):
        self.monday, self.tuesday, self.wednesday, self.thursday, \
            self.friday, self.saturday, self.sunday = days

    def __iter__(self):
        for day in [self.monday, self.tuesday, self.wednesday,
                    self.thursday, self.friday, self.saturday,
                    self.sunday]:
            yield day
