from flask import Blueprint, redirect, request
from flask_login import login_required, current_user

from common import admin_required
from models import Run, Apply

blueprint = Blueprint('run_page', __name__)


@blueprint.route('/post', methods=['POST'])
@admin_required
def post():
    Run(title=request.form['data']).save()
    return redirect('/')


@blueprint.route('/apply', methods=['POST'])
@login_required
def apply():
    Apply(post_id=request.form['post_id'], user_id=current_user.user_id).save()
    return redirect('/')
