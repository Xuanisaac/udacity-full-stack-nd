from user import User
from google.appengine.ext import db


class Like(db.Model):
    post_id = db.StringProperty(required=True)
    author = db.StringProperty(required=True)

    def getUserName(self):
        user = User.by_id(self.user_id)
        return user.name
