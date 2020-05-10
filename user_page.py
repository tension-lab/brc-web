from flask import Blueprint, render_template, redirect, request

from common import admin_required
from models import User

blueprint = Blueprint('user_page', __name__)


@blueprint.route('/member')
@admin_required
def user_list():
    users = User.objects(is_member=True).order_by('+is_admin', '+nickname')
    return render_template('user_list.html', users=users)


@blueprint.route('/guest')
@admin_required
def guest():
    users = User.objects(is_member__ne=True)
    return render_template('user_list.html', users=users)


@blueprint.route('/promote', methods=['POST'])
@admin_required
def promote():
    User.objects(user_id=request.form['user_id']).update_one(is_member=True)
    return redirect('/guest')


@blueprint.route('/leave', methods=['POST'])
@admin_required
def leave():
    User.objects(user_id=request.form['user_id']).update_one(is_member=False)
    return redirect('/member')
