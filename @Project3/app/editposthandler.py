from bloghandler import BlogHandler
from models.user import User
from models.post import Post
from helper import *
from google.appengine.ext import db


class EditPost(BlogHandler):
    def get(self):
        if self.user:
            self.render("editpost.html")
        else:
            self.redirect("/login")
        return

    def post(self):
        if not self.user:
            self.redirect('/blog')
            return
        author = self.get_user_name()
        post_id = self.request.get('post_id')
        post_id = int(post_id)
        post = self.find_post_from_db(post_id)
        subject = self.request.get('subject')
        content = self.request.get('content')

        if not post_id:
            self.redirect('/blog/newpost')
            return

        if not post:
            self.error(404)
            return

        if post.author != author:
            msg = "Oops, you are not the author of this post"
            self.render('login-form.html', error=msg)
            return

        if subject and content:
            post.subject = subject
            post.content = content
            post.put()
            self.redirect('/blog/%s' % str(post.key().id()))
            return
        else:
            error = "subject and content, please!"
            self.render("editpost.html", subject=subject,
                        content=content, error=error)
            return
