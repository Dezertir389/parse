from flask import Flask, request, render_template, redirect, url_for
from data import db_session
from data.users import User
from data.flowers import Flowers
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/sign_in')
def log():
    return render_template('sign_in.html')


@app.route('/sign_up', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('sign_up.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect(f'/user_page/{form.email.data}')
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
    inf = (flow.png, flow.name, flow.about, flow.mid_price, flow.links)
    print(flow.png)
    return render_template('info.html', item=inf)


@app.route('/user_page/<email>')
def upage(email):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == email).first()
    inf = (user.name, user.about, user.email, user.created_date)
    return render_template('user_page.html', item=inf)


def main():
    db_session.global_init("db/Flowers.db")


if __name__ == '__main__':
    main()
    app.run()
