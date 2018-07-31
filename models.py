from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin

# create an instance of SQLAlchemy and LoginManager to pass on to run.py
db = SQLAlchemy()
# TODO: shift login manager to run.py
login_manager = LoginManager()
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

users = db.Table('users',
    db.Column('thread_id', db.Integer, db.ForeignKey('thread.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

# database schema for users
class User(UserMixin, db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    # threads = db.relationship('Thread', secondary=threads, lazy='subquery',
    #     backref=db.backref('users', lazy=True))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # function thats called when object is prointed
    # useful for debugging
    def __repr__(self):
        return '<User: {}>'.format(self.username)   



# user sends message to thread
class Thread(db.Model):

    __tablename__ = "thread"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    messages = db.relationship('Message', backref='thread', lazy=True)
    users = db.relationship('User', secondary=users, lazy='subquery',
        backref=db.backref('threads', lazy=True))

    def __repr__(self):
        return '<Thread: {}>'.format(self.id) 


# class ThreadParticipants(db.Model):
#      __tablename__ = "thread_participant"

#     id = db.Column(db.Integer, primary_key=True)
#     thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), primary_key=True)
#     user_id = 

#     def __repr__(self):
#         return '<Thread: {}>'.format(self.id) 

# messages in each thread
class Message(db.Model):

    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), primary_key=True)
    author_id = db.Column(db.Integer, default=User.id)
    message_text = db.Column(db.String(1000))
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message: {}>'.format(self.message_text) 