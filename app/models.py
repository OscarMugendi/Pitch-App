from datetime import datetime
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager


@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255),unique=True, index=True)
    email = db.Column(db.String(255),unique=True, index=True)
    encryptedpassword = db.Column(db.String(255), index=True)
    pitches = db.relationship('Pitch', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic') 
    
    @property
    def set_password(self):
        raise AttributeError('Encrypted')

    @set_password.setter
    def password(self, password):
        self.encryptedpassword = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.encryptedpassword,password) 
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f'User{self.username}'

class Pitch(db.Model):
    __tablename__ = 'pitches'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    pitch = db.Column(db.String(1000))
    comments = db.relationship('Comment',backref='pitch_id',lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def save_pitch(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_pitches(cls,id):
        pitches = Pitch.query.filter_by(id=id).all()
        return pitches

    @classmethod
    def get_pitch(cls,id):
        pitch = Pitch.query.filter_by(id=id).first()

        return pitch

    @classmethod
    def count_pitches(cls,uname):
        user = User.query.filter_by(username=uname).first()
        pitches = Pitch.query.filter_by(user_id=user.id).all()

        pitches_count = 0
        for pitch in pitches:
            pitches_count += 1

        return pitches_count


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String(1000))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    pitch = db.Column(db.Integer,db.ForeignKey("pitches.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,pitch):
        comments = Comment.query.filter_by(pitch_id=pitch).all()
        return comments
    
