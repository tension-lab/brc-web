from functools import wraps

from flask_login import current_user, login_required


def admin_required(func):
    @login_required
    @wraps(func)
    def decorated():
        if not current_user.is_admin:
            return '권한이 없어... 돌아가...', 401
        return func()

    return decorated


def member_required(func):
    @login_required
    @wraps(func)
    def decorated():
        if not current_user.is_member:
            return '권한이 없어... 돌아가...', 401
        return func()

    return decorated
