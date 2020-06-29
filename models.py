from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('run.id'), primary_key=True)
    nickname = db.Column(db.String)
    thumbnail = db.Column(db.String)
    is_member = db.Column(db.Boolean)
    is_admin = db.Column(db.Boolean)

    is_authenticated = True
    is_active = True
    is_anonymous = False

    def get_id(self):
        return self.id


class Run(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    time = db.Column(db.DateTime)
    applies = db.relationship('Apply')
    group_id = db.Column(db.String)
    description = db.Column(db.String)


class Apply(db.Model):
    run_id = db.Column(db.Integer, db.ForeignKey('run.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    time = db.Column(db.DateTime)
    user = db.relationship('User')
    # no_show = db.BooleanField()
