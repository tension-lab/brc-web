from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String)
    thumbnail = db.Column(db.String)
    is_member = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    is_authenticated = True
    is_active = True
    is_anonymous = False

    def get_id(self):
        return self.id


class Run(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    time = db.Column(db.DateTime)
    group_id = db.Column(db.String)
    description = db.Column(db.String)


class Apply(db.Model):
    run_id = db.Column(db.Integer, db.ForeignKey('run.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    time = db.Column(db.DateTime, nullable=False)
    approved = db.Column(db.Boolean, nullable=True)
    user = db.relationship('User')
    run = db.relationship('Run')
    # no_show = db.BooleanField()


class Bingo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    image = db.Column(db.String, nullable=False)
    check = db.Column(db.Boolean)
    user = db.relationship('User')
