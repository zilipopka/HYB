from langchain_core.messages import HumanMessage, SystemMessage

from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from sweater import *

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

        return redirect(f'/sign_in')

    else:
        return render_template("sign_up.html")


@app.route('/')
@app.route('/home')
def home():
    return render_template('homepage.html')



@app.route('/new_request', methods=['POST', 'GET'])
@login_required
def index():
    if request.method == "POST":
        information = request.form['info']
        task = f"Сейчас я опишу тебе компанию и ее деятельность. {information}. Придумай стратегию для развития этого бизнеса"
        messages = [HumanMessage(content=task)]
        response = model.invoke(messages)
        response = response.content.replace('###', '').replace('**', '')

        question = Requests(question=information, answer=response, token=current_user.token)
        db.session.add(question)
        db.session.commit()
        return render_template('main.html', response=response)
    else:
        return render_template("main.html")


@app.route('/requests')
@login_required
def requests():
    your_requests = Requests.query.filter_by(token=current_user.token).all()
    return render_template('main.html', requests=your_requests)


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        user = Users.query.filter_by(login=login).first()
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                login_user(user)
                next_page = request.args.get('next')

                return redirect('/user')

            else:
                return 'Error! Password is wrong!'
        else:
            return 'Error! Such login doesnt exist'
    else:
        return render_template('sign_in.html')


@app.route('/user')
@login_required
def user():
    return render_template('main.html')


@app.route('/logout')
@login_required
def log_out():
    logout_user()
    return redirect('/')