from flask_mongoengine import MongoEngine

db = MongoEngine()


class User(db.Document):
    user_id = db.StringField()
    nickname = db.StringField()

    def is_active(self):
        return self.is_active

    def get_id(self):
        return self.user_id

    def is_authenticated(self):
        return self.authenticated
