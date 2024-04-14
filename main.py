from flask import Flask, request, jsonify, render_template
import json
import requests
from data import db_session
from data.flowers import Flowers

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

is_log = False




@app.route('/sign_in')
def log():
    return render_template('sign_in.html')


@app.route('/sign_up')
def log_ib():
    return render_template('sign_up.html')


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
    db_session.global_init("db/blogs.db")


if __name__ == '__main__':
    main()
    app.run()
