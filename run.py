from flask import Flask, render_template, url_for, flash, redirect, request, abort
from config import Config
from forms import LoginForm, SignUpForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.urls import url_parse
from models import db, User, login_manager
from flask_login import current_user, login_user, logout_user, login_required

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object(Config)
db.init_app(app)
# migrate = Migrate(app, db)
login_manager.init_app(app)

#initialize database tables once
def init():
    with app.app_context():
        db.create_all()

@app.route('/index')
@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # if a logged in user tries to go to /signup
    # redirect the user to index
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    signup_form = SignUpForm()
    if signup_form.validate_on_submit():
        user = User(username=signup_form.username.data, 
            email=signup_form.email.data)
        user.set_password(signup_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations! You are now a registered user.")
        return redirect(url_for('login'))

    return render_template('signup.html', title='Sign Up', signup_form=signup_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # if a logged in user tries to go to /login
    # redirect the user to index
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    login_form = LoginForm()
    if login_form.validate_on_submit():

        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash("Incorrect Username or Password")
            return redirect(url_for('login'))

        login_user(user,remember = login_form.remember_me.data)
        flash('Logged in successfully.')
        next_page = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Login', login_form = login_form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    #init()
    app.run()
