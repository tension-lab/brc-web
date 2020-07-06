from flask_admin.contrib import sqla
from flask_login import current_user


class AdminModelView(sqla.ModelView):
    def is_accessible(self):
        return current_user.is_admin
