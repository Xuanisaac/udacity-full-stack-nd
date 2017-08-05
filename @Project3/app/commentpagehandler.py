from bloghandler import BlogHandler
from models.user import User
from models.post import Post
from models.like import Like
from models.comment import Comment
from helper import *
from google.appengine.ext import db


class CommentPage(BlogHandler):
    """docstring for ClassName"""
    def find_post_from_db(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        if not post:
            self.error(404)
            return
        return post

    def get_comment_by_id(self, comment_id):
        key = db.Key.from_path('Comment', int(comment_id))
        comment = db.get(key)
        if not comment:
            self.error(404)
            return
        return comment

    def delete_comment(self, comment, post_id):
        comment.delete()
        self.redirect('/blog/' + str(post_id))
        return

    def get(self, comment_id):
        self.redirect('/blog/%s' % comment_id)
        return

    def post(self, comment_id):
        if not self.user:
            msg = "Log in to modify comment sections"
            self.render('login-form.html', error=msg)
            return

        author = self.get_user_name()

        post_id = self.request.get('post_id')
        action = self.request.get("action")
        comment_id = int(comment_id)
        post_id = int(post_id)
        comment = self.get_comment_by_id(comment_id)
        post = self.find_post_from_db(post_id)

        if not comment:
            self.write("no comment")
            return

        if comment.author != author:
            msg = "Oops, you are not the author of this comment"
            self.render('login-form.html', error=msg)
            return

        if action == "delete":
            self.delete_comment(comment, post_id)

        elif action == "edit":
            content = comment.content
            self.render("editcomment.html", post=post, numoflikes=0,
                        comment_ins=comment, content=comment.content)
            return
