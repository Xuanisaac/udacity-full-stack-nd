from bloghandler import BlogHandler

from helper import *
from google.appengine.ext import db


class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/blog')
        return
