from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin

# create an instance of SQLAlchemy and LoginManager to pass on to run.py
db = SQLAlchemy()
login_manager = LoginManager()
login.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# database schema for users
class User(UserMixin, db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    messages = db.Relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # function thats called when object is prointed
    # useful for debugging
    def __repr__(self):
        return '<User: {}>'.format(self.username)   

class Post(db.Model):

    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    message_text = db.Column(db.String(1000))
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Message: {}>'.format(self.message_text) 