from langchain_gigachat.chat_models import GigaChat
from flask import Flask, render_template, request, redirect
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import string
import random
import bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import timedelta

load_dotenv()

model = GigaChat(
    credentials=os.getenv('CREDENTIALS'),
    scope=os.getenv('SCOPE'),
    model=os.getenv('MODEL'),
    verify_ssl_certs=False
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRES_CONN')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.secret_key = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.after_request
def redirect_to_sign_in(response):
    if response.status_code == 401:
        return redirect(('/sign_in') + '?next=' + request.url)

    return response


def generate_token():
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(50))
    return token

def hash_pass(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    return hashed

class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    token = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Users %r>' % self.id


class Requests(db.Model):
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    token = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Requests %r>' % self.id
