from datetime import datetime

from flask import Blueprint, redirect, request, render_template
from flask_login import login_required, current_user

from common import admin_required
from models import Run, Apply, db

blueprint = Blueprint('run_page', __name__)


@blueprint.route('/run/write', methods=['POST'])
@admin_required
def post():
    run = Run(title=request.form['data'], time=datetime.now())
    db.session.add(run)
    db.session.commit()
    return redirect('/')


@blueprint.route('/run/apply', methods=['POST'])
@login_required
def do_apply():
    apply = Apply(run_id=request.form['run_id'], user_id=current_user.id)
    db.session.add(apply)
    db.session.commit()
    return redirect('/run/' + request.form['run_id'])


@blueprint.route('/run/<run_id>')
def run_detail(run_id):
    run = Run.query.filter_by(id=run_id).first()
    if run is None:
        return '없어진 달리기...'
    is_apply = False
    for apply in run.applies:
        if apply.user_id == current_user.id:
            is_apply = True
            break
    return render_template('run_detail.html', run=run, is_apply=is_apply)
