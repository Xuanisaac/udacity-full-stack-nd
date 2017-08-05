from app.bloghandler import BlogHandler
from models.user import User
from models.post import Post
from helper import *
from google.appengine.ext import db


class BlogFront(BlogHandler):
    def delete_post(self, post_instance):
        post_instance.delete()
        self.redirect('/blog')
        return

    def get(self):
        posts = greetings = Post.all().order('-created')
        self.render('front.html', posts=posts)

    def post(self):
        if not self.user:
            msg = "Log in to modify posts"
            self.render('login-form.html', error=msg)
            return

        author = self.get_user_name()

        post_id = self.request.get('post_id')
        post_id = int(post_id)
        action = self.request.get("action")

        post = self.find_post_from_db(post_id)

        if post.author != author:
            msg = "Oops, you are not the author of this post"
            self.render('login-form.html', error=msg)
            return

        if action == "delete":
            self.delete_post(post)

        elif action == "edit":
            post = self.find_post_from_db(post_id)
            subject = post.subject
            content = post.content

            self.render("editpost.html", subject=subject,
                        content=content, post_id=post_id)
            return
