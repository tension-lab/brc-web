from flask import Blueprint, redirect, render_template
from flask_login import login_user

from common import admin_required
from models import User, db

blueprint = Blueprint('debug_page', __name__)


@blueprint.route('/debug')
@admin_required
def debug():
    return render_template('debug.html')


@blueprint.route('/debug/add_user')
@admin_required
def add_user():
    from datetime import datetime
    user_id = datetime.utcnow().strftime('%m%d%H%M%S')
    user = User(id=int(user_id), nickname=user_id, is_member=False, is_admin=True)
    db.session.add(user)
    db.session.commit()
    login_user(user, remember=True)
    return redirect('/')
