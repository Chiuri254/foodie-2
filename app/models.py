# from builtins import classmethod
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
from time import time

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(40),unique = True, index=True)
    hash_pass = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True, index = True)

    feedback = db.relationship('Intcom',backref='user',lazy='dynamic')
    comments = db.relationship('Comment',backref='user',lazy='dynamic')


    @property
    def password(self):
        raise AttributeError("You cannot read password attribute")

    @password.setter
    def password(self,password):
        self.hash_pass = generate_password_hash(password)

    def set_password(self,password):
        self.hash_pass = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.hash_pass,password)

    def __repr__(self):
        return f'User {self.username}'

class Intcom(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer,primary_key = True)
    feed_content = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_comm(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comms(cls,id):
        data = Intcom.query.filter_by(id=id).all()
        return data

    @classmethod
    def get_all_comms(cls):
        data = Intcom.query.order_by('-id').all()
        return data

class Comment(db.Model):
    __tablename__='comments'

    id = db.Column(db.Integer,primary_key=True)
    comment_content = db.Column(db.String())
    pitch_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(pitch_id=id).all()
        return comments
