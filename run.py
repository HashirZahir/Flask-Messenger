from flask import Flask, render_template, flash, redirect, request, abort
from config import Config
import forms
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User, login_manager
from flask_login import current_user, login_user, logout_user

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object(Config)
db.init_app(app)
# migrate = Migrate(app, db)
login_manager.init_app(app)

@app.route('/index')
@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # if a logged in user tries to go to /login
    # redirect the user to index
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    login_form = forms.LoginForm()
    if login_form.validate_on_submit():

        user = User.query.filter_by(username=login_form.username.data).first()
        if not user.check_password(login_form.password.data) or user is None:
            flash("Incorrect Username or Password")
            return redirect(url_for('login'))

        login_user(user,remember = login_form.remember_me.data)
        flash('Logged in successfully.')
        next_page = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        if not is_safe_url(next_page):
            return abort(400, "Unsafe URL")
        return redirect(url_for('/index'))
    return render_template('login.html', login_form = login_form)

@app.route('/logout'):
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
