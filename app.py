import os

import flask_login
import requests
from flask import Flask, render_template, request, redirect, json
from flask_admin import Admin
from flask_login import login_user, logout_user

import bingo_page
import debug_page
import run_page
import user_page
from admin import AdminModelView
from models import db, User, Run, Apply, Bingo

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(user_page.blueprint)
app.register_blueprint(run_page.blueprint)
app.register_blueprint(bingo_page.blueprint)
app.register_blueprint(debug_page.blueprint)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

db.init_app(app)
admin = Admin(app, template_mode='bootstrap3')
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Run, db.session))
admin.add_view(AdminModelView(Apply, db.session))
admin.add_view(AdminModelView(Bingo, db.session))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    data = json.loads(request.form['data'])
    access_token = data['access_token']
    res = requests.get('https://kapi.kakao.com/v2/user/me', headers={'Authorization': f'Bearer {access_token}'})
    me = res.json()
    user_id = str(me['id'])
    profile = me['kakao_account']['profile']
    nickname = profile['nickname']
    thumbnail = None
    if 'thumbnail_image_url' in profile:
        thumbnail = me['kakao_account']['profile']['thumbnail_image_url'].replace("http://", "https://", 1)
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        user = User(id=user_id, nickname=nickname, thumbnail=thumbnail)
        db.session.add(user)
        db.session.commit()
    else:
        if user.thumbnail != thumbnail:
            user.thumbnail = thumbnail
            db.session.commit()
    login_user(user, remember=True)

    return redirect('/')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ['PORT'])
