from flask_mongoengine import MongoEngine

db = MongoEngine()


class User(db.Document):
    user_id = db.StringField()
    nickname = db.StringField()
    thumbnail = db.StringField()
    is_member = db.BooleanField()
    is_admin = db.BooleanField()
    is_dev = db.BooleanField()

    def is_active(self):
        return self.is_active

    def get_id(self):
        return self.user_id

    def is_authenticated(self):
        return self.authenticated


class Run(db.Document):
    title = db.StringField()
    # group = db.ListField(db.StringField())
    # content = db.StringField()


class Apply(db.Document):
    post_id = db.StringField()
    user_id = db.StringField()
    user = db.ReferenceField(User)
    # no_show = db.BooleanField()
