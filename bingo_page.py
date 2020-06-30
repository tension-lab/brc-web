import os
from datetime import datetime

from flask import Blueprint, render_template, request, redirect
from flask_login import current_user

from common import member_required, admin_required
from models import Bingo, db

blueprint = Blueprint('bingo_page', __name__)


@blueprint.route('/bingo')
@member_required
def bingo_main():
    bingo_all = Bingo.query.filter_by(user_id=current_user.id, check=True)
    success_list = list()
    for bingo in bingo_all:
        if bingo.number not in success_list:
            success_list.append(bingo.number)
    return render_template('bingo.html', success_list=success_list, description=description)


@blueprint.route('/bingo/<number>')
@member_required
def bingo_detail(number):
    bingo = Bingo.query.filter_by(user_id=current_user.id, number=number).first()
    return render_template('bingo_detail.html', number=number, bingo=bingo)


@blueprint.route('/bingo/<number>/upload', methods=['POST'])
@member_required
def do_upload(number):
    f = request.files.get('file')
    folder = os.path.join('static', 'bingo', str(current_user.id))
    filename = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    f.save(path)
    path = os.path.join('/', path)
    bingo = Bingo.query.filter_by(user_id=current_user.id, number=number).first()
    if bingo:
        bingo.time = datetime.now()
        bingo.image = path
    else:
        bingo = Bingo(user_id=current_user.id, number=number, time=datetime.now(), image=path)
        db.session.add(bingo)
    db.session.commit()
    return 'OK'


@blueprint.route('/bingo/admin')
@admin_required
def bingo_admin():
    bingo = Bingo.query.filter_by(check=None).order_by(Bingo.time).first()
    return render_template('bingo_admin.html', bingo=bingo, description=description)


@blueprint.route('/bingo/admin/success')
@admin_required
def success():
    bingo = Bingo.query.filter_by(check=None).order_by(Bingo.time).first()
    bingo.check = True
    db.session.commit()
    return redirect('/bingo/admin')


@blueprint.route('/bingo/admin/fail')
@admin_required
def fail():
    bingo = Bingo.query.filter_by(check=None).order_by(Bingo.time).first()
    bingo.check = False
    db.session.commit()
    return redirect('/bingo/admin')


description = [
    "① 까치런 달리기(지도 공유)",
    "② 분당구청-아트센터 달리기",
    "③ 서현역-율동공원 찍고오기",
    "④ 트랙 5K 달리기",
    "⑤ 정기런 3주 연속 참여하기",
    "⑥ 오전 9시 이전에 러닝 시작하기",
    "⑦ 탄천트랙-아브뉴프랑 달리기(주말)",
    "⑧ 미금교-백궁교 왕복 달리기",
    "⑨ 황새울공원-판교역 찍고오기(평일)",
    "⑩ 율동공원 호수 4바퀴 달리기",
    "⑪ 야탑역-미금역 성남대로 따라 7.5K 달리기(각 역별 사진 콜라쥬 인증)",
    "⑫ 15K LSD 하기(야외)",
    "⑬ ~8월 31일까지 120K 달리기",
    "⑭ 일주일에 3일 이상 달리기하기(일-토 기준)",
    "⑮ 6월에 6K 달리기",
    "⑯ 판교역 출발 5K 달리기",
    "⑰ 번개런 호스트/프로그램 진행하기(평일)",
    "⑱ 안쉬고 3K 달리기",
    "⑲ WAKE-UP BUNDANG 참여하기(주말)",
    "⑳ BRC 815 마라톤 참석하기",
    "㉑ 크루티 입고 정기런 참여하기",
    "㉒ 평소 정기런 페이스 보다 1분 앞당겨 1K 달리기",
    "㉓ 수내역-판교도서관 달리기",
    "㉔ 8월달에 8K 달리기",
    "㉕ 구미동 3K 달리기(구미동 시작/종료)"
]
