from datetime import datetime
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True, index=True)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False, index=True)
    #pitches = db.relationship('Pitch', backref='user', lazy='dynamic')
    #comment = db.relationship('Comment', backref='user', lazy='dynamic')
    #upvote = db.relationship('Upvote',backref='user',lazy='dynamic')
    #downvote = db.relationship('Downvote',backref='user',lazy='dynamic')

    secure_password = db.Column(db.String(255))

    @property
    def set_password(self):
        raise AttributeError('You cannot read the password attribute')

    @set_password.setter
    def password(self, password):
        self.secure_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.secure_password,password) 
    
    def __repr__(self):
        return f'User {self.username}'


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))
