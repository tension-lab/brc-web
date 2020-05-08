from bson import ObjectId
from flask import Blueprint, redirect, request, render_template
from flask_login import login_required, current_user

from common import admin_required
from models import Run, Apply, User

blueprint = Blueprint('run_page', __name__)


@blueprint.route('/run/write', methods=['POST'])
@admin_required
def post():
    Run(title=request.form['data']).save()
    return redirect('/')


@blueprint.route('/run/apply', methods=['POST'])
@login_required
def apply():
    user = User(id=ObjectId(current_user.id))
    print(user)
    Apply(post_id=request.form['post_id'], user_id=current_user.user_id, user=user).save()
    return redirect('/run/' + request.form['post_id'])


@blueprint.route('/run/<run_id>')
def run_detail(run_id):
    run = Run.objects(id=run_id).first()
    if run is None:
        return '없어진 달리기...'
    applies = Apply.objects(post_id=run_id).all()
    return render_template('run_detail.html', run=run, applies=applies)
