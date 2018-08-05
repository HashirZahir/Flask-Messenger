from flask import Flask, render_template, url_for, flash, redirect, request, abort
from config import Config
from forms import LoginForm, SignUpForm, ChatWithForm, ChatForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.urls import url_parse
from models import db, User, Message, Thread, users, login_manager
from flask_login import current_user, login_user, logout_user, login_required
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object(Config)
db.init_app(app)
# migrate = Migrate(app, db)
login_manager.init_app(app)

#initialize database tables once
def init():
    with app.app_context():
        db.create_all()

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    chatwith_form = ChatWithForm()
    if chatwith_form.validate_on_submit():
        user = User.query.filter_by(
            username=chatwith_form.username.data).first()

        if user is None:
            flash("User does not exist")
        else:
            # minor bug: chatting with yourself shows messages of 1st thread created
            threads_user = db.session.query(users).filter_by(user_id=user.id).all()
            threads_current_user = db.session.query(users).filter_by(user_id=current_user.id).all()
            for thread_user in threads_user:
                for thread_current_user in threads_current_user:
                    if thread_user.thread_id == thread_current_user.thread_id:
                        return redirect(url_for('chat', thread_id=thread_user.thread_id))
            
            thread = Thread(name=user.username)
            thread.users.append(user)
            thread.users.append(current_user)
            db.session.add(thread)
            db.session.commit()
            return redirect(url_for('chat', thread_id=thread.id))
    return render_template('index.html', title='Chat', chatwith_form=chatwith_form, thread=None)

@app.route('/<int:thread_id>', methods=['GET', 'POST'])
@login_required
def chat(thread_id):
    thread = Thread.query.get(thread_id)
    logger.info('thread: %s', thread_id)
    chat_form = ChatForm()
    chatwith_form = ChatWithForm()
    if thread is None:
        flash('Error: No such user')
        return redirect(url_for('index'))  
    if chat_form.validate_on_submit():
        # TODO: implement insertion and update DB
        message = Message(message_text=chat_form.message_text.data, author_id=current_user.id)
        thread.messages.append(message)
        db.session.add(thread)
        db.session.commit()
    return render_template('index.html', title='Chat', chatwith_form=chatwith_form, 
                                                                chat_form=chat_form,thread=thread) 


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
        # check if the url is safe for redirects.
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Login', login_form = login_form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    init()
    app.run()
