import webapp2
from string import letters
from google.appengine.ext import db
from helper import *
from models.post import Post
from models.user import User
from models.comment import Comment
from models.like import Like

from app.bloghandler import BlogHandler
from app.blogfronthandler import BlogFront
from app.commentpagehandler import CommentPage
from app.editcommenthandler import EditComment
from app.editposthandler import EditPost
from app.likeposthandler import LikePost
from app.loginhandler import Login
from app.logouthandler import Logout
from app.newposthandler import NewPost
from app.postpagehandler import PostPage
from app.registerhandler import Register
from app.signuphandler import Signup


def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)


class MainPage(BlogHandler):
    def get(self):
        self.render('mainpage.html')


class Unit3Welcome(BlogHandler):
    def get(self):
        if self.user:
            self.render('welcome.html', username=self.user.name)
        else:
            self.redirect('/signup')


class Welcome(BlogHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username=username)
        else:
            self.redirect('/unit2/signup')


class ContactPage(BlogHandler):
    def get(self):
        self.render('contactme.html')


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/contactme', ContactPage),
                               ('/blog/?', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ('/blog/editpost', EditPost),
                               ('/like/([0-9]+)', LikePost),
                               ('/comment/([0-9]+)', CommentPage),
                               ('/comment/editcomment/([0-9]+)', EditComment),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               ],
                              debug=True)
