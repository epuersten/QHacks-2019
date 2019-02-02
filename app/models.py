from flask import Flask
from app import app, db, login

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from time import time
import jwt


# DATA TYPES
# https://sqlalchemy-html.readthedocs.io/en/rel_1_0_6/core/type_basics.html#sql-standard-types


# Video on back ref syntax: see 14:05: https://www.youtube.com/watch?v=juPQ04_twtA

@login.user_loader
def load_user(user_id):
    return NetUser.query.get(int(user_id))



class NetUser(UserMixin, db.Model):

    __tablename__ = 'net_user'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    first_name = db.Column(db.String(75))
    last_name = db.Column(db.String(75))

    first_name = db.Column(db.String(75))
    last_name = db.Column(db.String(75))

    school_name = db.Column(db.String(75))
    program_name = db.Column(db.String(75))

    def __repr__(self):
        return '<NetUser {}>'.format(self.email)

    # Work around for UserMixin to allow user_id instead of just id:
    # https://stackoverflow.com/questions/37472870/login-user-fails-to-get-user-id
    def get_id(self):
        return (self.user_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    # def get_reset_password_token(self, expires_in=600):
    #     return jwt.encode(
    #         {'reset_password': self.user_id, 'exp': time() + expires_in},
    #         app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    # @staticmethod
    # def verify_reset_password_token(token):
    #     try:
    #         user_id = jwt.decode(token, app.config['SECRET_KEY'],
    #                         algorithms=['HS256'])['reset_password']
    #     except:
    #         return
    #     return NetUser.query.get(user_id)
