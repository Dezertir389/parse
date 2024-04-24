from flask import Flask, request, render_template, redirect, url_for
from data import db_session
from data.users import User
from data.flowers import Flowers
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, login_required,logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/us_page/<id>')
def us_page(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == id).first()
    inf = (user.id, user.name, user.about, user.email)
    return render_template('user_page.html', item=inf)


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(f"/us_page/{user.id}")
        return render_template('sign_in.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('sign_in.html', title='Авторизация', form=form)



@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('sign_up.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('sign_up.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect(f'/us_page/{user.id}')
    return render_template('sign_up.html', title='Регистрация', form=form)


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
