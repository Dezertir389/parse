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


@app.route('/login', methods=['POST'])
def login():
    login = request.form.get('login')
    password = request.form.get('password')

    user = db_session.query(User).filter(User.login == login, User.password == password).first()
    if user:
        session['user_login'] = login
        return 'Вы успешно вошли'
    else:
        return 'Неверный логин или пароль'


@app.route('/')
def main_page():
    li = []
    db_sess = db_session.create_session()
    for flow in db_sess.query(Flowers).all():
        li.append((flow.png, flow.name, flow.mid_price))
    return render_template('search.html', inf=li)


@app.route('/info/<title>')
def info(title):
    db_sess = db_session.create_session()
    flow = db_sess.query(Flowers).filter(Flowers.name == title).first()
    inf = (flow.name, flow.about, flow.mid_price, flow.links, flow.png)
    return render_template('info.html', item=inf)


def main():
    db_session.global_init("db/Flowers.db")


if __name__ == '__main__':
    main()
    app.run()
