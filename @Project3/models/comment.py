from user import User
from google.appengine.ext import db


class Comment(db.Model):
    author = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    postid = db.StringProperty(required=True)
    user_id = db.IntegerProperty(required=True)

    def getUserName(self):
        user = User.by_id(self.user_id)
        return user.name
