from flask import Flask, render_template, redirect, request
from data import db_session
from data.users import User
from data.flowers import Flowers
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
lia = []


@app.route('/add_wish/<name>')
def add_wish(name):
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if bool(user.flowers):
        if name not in user.flowers.split(';') + [name]:
            user.flowers = ';'.join(user.flowers.split(';') + [name])
    else:
        user.flowers = name
    db_sess.commit()
    return redirect(f"/info/{name}")


@app.route('/del_wish/<name>')
def del_wish(name):
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if len(user.flowers.split(';')) == 1:
        user.flowers = ''
        db_sess.commit()
    elif len(user.flowers.split(';')) == 2:
        n = user.flowers.split(';')
        n.remove(name)
        user.flowers = ''.join(n)
        db_sess.commit()
    else:
        n = user.flowers.split(';')
        n.remove(name)
        user.flowers = ';'.join(n)
        db_sess.commit()
    return redirect(f"/info/{name}")



@login_manager.user_loader
def load_user(user_id):
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/us_page/<id>')
@login_required
def us_page(id):
    user = db_sess.query(User).filter(User.id == id).first()
    inf = (user.id, user.name, user.about, user.email)
    return render_template('user_page.html', item=inf, title=f'{user.name}')


@app.route('/favorites/<id>')
@login_required
def us_page_fav(id):
    user = db_sess.query(User).filter(User.id == id).first()
    li = []
    if bool(user.flowers):
        for flow in db_sess.query(Flowers).all():
            if flow.name in user.flowers:
                li.append((flow.png, flow.name, flow.mid_price))
    inf = (li, user.name, user.id)
    return render_template('user_page_fav.html', item=inf, title=f'{user.name}')


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = LoginForm()
    if form.validate_on_submit():
        sss = db_sess.query(User).filter(User.email == form.email.data).first()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            lia.append((form.password.data, form.email.data))
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
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
        return redirect(f'/sign_in')
    return render_template('sign_up.html', title='Регистрация', form=form)


@app.route('/')
def main_page():
    print(lia)
    li = []
    for flow in db_sess.query(Flowers).all():
        li.append((flow.png, flow.name, flow.mid_price))
    li = sorted(li, key=lambda x: x[1])
    return render_template('search.html', inf=li, title='Свежая жизнь')


@app.route('/info/<title>')
def info(title):
    n = None
    if current_user.is_authenticated:
        n = db_sess.query(User).filter(User.id == current_user.id).first()
    flow = db_sess.query(Flowers).filter(Flowers.name == title).first()
    inf = (flow.name, flow.about, flow.mid_price, flow.links, flow.png)
    if bool(n) and bool(n.flowers):
        return render_template('info.html',
                               item=inf, wish=flow.name in n.flowers, title=f'{flow.name}')
    return render_template('info.html', item=inf, wish=False, title=f'{flow.name}')


@app.route('/info_uh/<title>')
def info_uh(title):
    flow = db_sess.query(Flowers).filter(Flowers.name == title).first()
    inf = (flow.png, flow.uhod, flow.name)
    return render_template('info_uhod.html', item=inf, title=f'{flow.name}')



def main():
    db_session.global_init("db/Flowers.db")


if __name__ == '__main__':
    main()
    db_sess = db_session.create_session()
    app.run()
