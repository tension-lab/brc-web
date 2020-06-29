from flask import Blueprint, render_template, redirect, request

from common import admin_required
from models import User, db

blueprint = Blueprint('user_page', __name__)


@blueprint.route('/member')
@admin_required
def user_list():
    users = User.query.filter_by(is_member=True).order_by(User.is_admin.desc(), User.nickname.desc())
    return render_template('user_list.html', users=users)


@blueprint.route('/guest')
@admin_required
def guest():
    users = User.query.filter_by(is_member=False)
    return render_template('user_list.html', users=users)


@blueprint.route('/promote', methods=['POST'])
@admin_required
def promote():
    user = User.query.filter_by(id=request.form['user_id']).first()
    user.is_member = True
    db.session.commit()
    return redirect('/guest')


@blueprint.route('/leave', methods=['POST'])
@admin_required
def leave():
    user = User.query.filter_by(id=request.form['user_id']).first()
    user.is_member = False
    db.session.commit()
    return redirect('/member')
