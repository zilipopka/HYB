from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
from flask import Flask, render_template, request, redirect
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import string
import random
import bcrypt

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

db = SQLAlchemy(app)


def generate_token():
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(50))
    return token

def hash_pass(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    return hashed

class Users(db.Model):
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


@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == "POST":
        login = request.form['login']
        if Users.query.filter_by(login=login).first():
            return 'Error! This login already exists'

        password = request.form['password']

        token = generate_token()
        while True:
            if Users.query.filter_by(token=token).first():
                token = generate_token()
            else:
                break

        user = Users(login=login, password=hash_pass(password), token=token)
        db.session.add(user)
        db.session.commit()

        return redirect(f'/{token}/requests')

    else:
        return render_template("sign_up.html")


@app.route('/')
@app.route('/home')
def home():
    return render_template('homepage.html')



@app.route('/<string:token>/new_request', methods=['POST', 'GET'])
def index(token):
    if request.method == "POST":
        information = request.form['info']
        task = f"Сейчас я опишу тебе компанию и ее деятельность. {information}. Придумай стратегию для развития этого бизнеса"
        messages = [HumanMessage(content=task)]
        response = model.invoke(messages)
        response = response.content.replace('###', '').replace('**', '')

        question = Requests(question=information, answer=response, token=token)
        db.session.add(question)
        db.session.commit()
        return render_template('output_2.html', response=response)
    else:
        return render_template("index_2.html")


@app.route('/<string:token>/requests')
def requests(token):
    your_requests = Requests.query.filter_by().all()
    return render_template('requests.html', requests=your_requests)


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        user = Users.query.filter_by(login=login).first()
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                token = user.token

            else:
                return 'Error! Password is wrong!'
        else:
            return 'Error! Such login doesnt exist'
        return redirect(f'/{token}/requests')
    else:
        return render_template('sign_in.html')





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
