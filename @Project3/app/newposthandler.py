from bloghandler import BlogHandler
from models.user import User
from models.post import Post
from models.like import Like
from models.comment import Comment
from helper import *
from google.appengine.ext import db


class NewPost(BlogHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            msg = "Please Login to Create Your Blog"
            self.render("login-form.html", error=msg)
        return

    def post(self):
        if not self.user:
            self.redirect('/blog')
            return
        subject = self.request.get('subject')
        content = self.request.get('content')
        post_id = self.request.get('post_id')

        author = self.get_uid()
        author = User.by_id(int(author))
        author = author.name

        if subject and content:
            p = Post(parent=blog_key(), subject=subject,
                     content=content, author=author)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject,
                        content=content, error=error)
        return
