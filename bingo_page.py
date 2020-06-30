import os

from flask import Blueprint, render_template, request
from flask_login import current_user

from common import member_required

blueprint = Blueprint('bingo_page', __name__)


@blueprint.route('/bingo')
@member_required
def bingo():
    return render_template('bingo.html')


@blueprint.route('/bingo/<number>')
@member_required
def bingo_upload(number):
    return render_template('bingo_upload.html', number=number)


@blueprint.route('/bingo/<number>/upload', methods=['POST'])
@member_required
def do_upload(number):
    f = request.files.get('file')
    folder = os.path.join('static', 'bingo', str(current_user.id))
    filename = str(number)
    os.makedirs(folder, exist_ok=True)
    f.save(os.path.join(folder, filename))
    return render_template('bingo_upload.html', number=number)
