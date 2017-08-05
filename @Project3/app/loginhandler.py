from bloghandler import BlogHandler
from models.user import User
from models.post import Post
from models.like import Like
from models.comment import Comment
from helper import *
from google.appengine.ext import db


class Login(BlogHandler):
    def get(self):
        self.render('login-form.html')
        return

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        redirect = self.request.get('redirection')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error=msg)
        return
