from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo, Length, ValidationError
from models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(),Length(min=5,max=20)])
    email = StringField('Email', validators=[InputRequired(), Email('Please enter valid email')])
    password = PasswordField("Password", validators=[InputRequired(),Length(min=6,max=20)])
    password_repeat = PasswordField("Repeat Password", 
        validators=[InputRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

    # custom validator following validate_<fieldname>
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please choose another username')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Account with this email already exists')