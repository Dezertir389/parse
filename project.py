from flask import Flask, request, jsonify, render_template, redirect, url_for
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route('/sign_in')
def log():
    return render_template('sign_in.html')

@app.route('/sign_up')
def log_ib():
    return render_template('sign_up.html')

@app.route('/register', methods=['POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')

    if db_session.query(User).filter(User.login == login).first():
        return 'Этот логин уже занят'

    # Создаем нового пользователя
    user = User(login=login, password=password)
    db_session.add(user)
    db_session.commit()

    return redirect(url_for('log'))
