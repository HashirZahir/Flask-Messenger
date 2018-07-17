from flask_sqlalchemy import SQLAlchemy

# create an instance of SQLAlchemy to pass on to run.py
db = SQLAlchemy()

# database schema for users
class User(db.Model):

    # table name in database
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # function thats called when object is prointed
    # useful for debugging
    def __repr__(self):
        return '<User {}>'.format(self.username)   