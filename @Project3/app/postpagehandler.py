from bloghandler import BlogHandler
from models.user import User
from models.post import Post
from models.like import Like
from models.comment import Comment
from helper import *
from google.appengine.ext import db


class PostPage(BlogHandler):

    def get_post_by_id(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        return post

    def get(self, post_id):
        post = self.get_post_by_id(post_id)
        if not post:
            self.error(404)
            return

        comments = Comment.gql("WHERE postid = '%s' " % (str(post_id)))
        numoflikes = Like.gql("WHERE post_id = '%s' " % (str(post_id))).count()
        self.render("permalink.html", post=post, comments=comments,
                    numoflikes=numoflikes)
        return

    def post(self, post_id):
        if not self.user:
            msg = 'Login to Make Comment to Post'
            self.render('login-form.html', error=msg)
            return

        post_id = self.request.get("post_id")
        comment_content = self.request.get("Comment")
        numoflikes = Like.gql("WHERE post_id = '%s' " % (str(post_id))).count()

        post = self.get_post_by_id(post_id)
        if not post:
            self.error(404)
            return

        if not comment_content:
            comments = Comment.gql("WHERE postid = '%s' " % (str(post_id)))
            msg = "Comment Cannot be Empty"
            self.render("permalink.html", post=post,
                        comments=comments, error=msg, numoflikes=numoflikes)
            return
        author_name = self.get_user_name()
        uid = self.get_uid()
        comment_ins = Comment(content=comment_content, postid=post_id,
                              author=author_name, user_id=uid)
        comment_ins.put()
        comments = Comment.gql("WHERE postid = '%s' " % (str(post_id)))

        self.render("permalink.html", post=post, comment_ins=None,
                    comments=comments, numoflikes=numoflikes)
        return
