from datetime import datetime

from flask import Blueprint, redirect, request, render_template
from flask_login import login_required, current_user

from common import admin_required
from models import Run, Apply, db

blueprint = Blueprint('run_page', __name__)


@blueprint.route('/run')
def run_list():
    run = Run.query.order_by(Run.time.desc()).first()
    is_apply = Apply.query.filter_by(run_id=run.id, user_id=current_user.id).first()
    return render_template('run_list.html', run=run, is_apply=is_apply)


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
    apply = Apply(run_id=request.form['run_id'], user_id=current_user.id, time=datetime.now())
    db.session.add(apply)
    db.session.commit()
    return redirect('/run')


@blueprint.route('/run/<run_id>')
@admin_required
def run_detail(run_id):
    run = Run.query.filter_by(id=run_id).first()
    if run is None:
        return '없어진 달리기...'
    apply_list = Apply.query.filter_by(run_id=run.id)
    return render_template('run_detail.html', run=run, apply_list=apply_list)


@blueprint.route('/run/<run_id>/apply/<user_id>')
@admin_required
def attend(run_id, user_id):
    apply = Apply.query.filter_by(run_id=run_id, user_id=user_id).first()
    if apply is None:
        return '참석하지 않음'
    apply.approved = True
    db.session.commit()
    return redirect(f'/run/{run_id}')


@blueprint.route('/run/<run_id>/noshow/<user_id>')
@admin_required
def no_show(run_id, user_id):
    apply = Apply.query.filter_by(run_id=run_id, user_id=user_id).order_by(Apply.approved).first()
    if apply is None:
        return '참석하지 않음'
    apply.approved = False
    db.session.commit()
    return redirect(f'/run/{run_id}')
