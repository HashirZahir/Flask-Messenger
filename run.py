from flask import Flask, render_template, flash, redirect
from config import Config
import forms
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object(Config)
db.init_app(app)
# migrate = Migrate(app, db)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = forms.LoginForm()
    if login_form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            login_form.username.data, login_form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', login_form = login_form)



if __name__ == '__main__':
    app.run()
