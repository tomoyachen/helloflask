# -*- coding: utf-8 -*-
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from watchlist import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(128))
    isAdmin = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class Api(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    path = db.Column(db.String(60))
    response = db.Column(db.String(60))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow(), index=True)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer) #1加分 2减分
    action = db.Column(db.String(60))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
