from bloghandler import BlogHandler
from models.user import User
from models.post import Post
from models.comment import Comment
from models.like import Like
from helper import *
from google.appengine.ext import db


class LikePost(BlogHandler):
    def get_post_by_id(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        return post

    def get(self, post_id):
        self.redirect("/blog/%s" % (str(post_id)))
        return

    def post(self, post_id):
        if not self.user:
            msg = 'Login to Like Post'
            self.render('login-form.html', error=msg)
            return

        post = self.get_post_by_id(post_id)
        if not post:
            self.error(404)
            return

        logged_name = self.get_user_name()

        numoflikes = Like.gql("WHERE post_id = '%s' " % (str(post_id))).count()
        if logged_name == post.author:
            comments = Comment.gql("WHERE postid = '%s' " % (str(post_id)))
            msg = "Oops, don't like your own post"

            self.render("permalink.html", post=post, comments=comments,
                        error=msg, numoflikes=numoflikes)
        else:
            like = Like.gql("WHERE post_id = '%s' AND author = '%s'" %
                            (str(post_id), logged_name)).count()
            if like == 0:
                new_like = Like(post_id=str(post_id), author=str(logged_name))
                new_like.put()
                numoflikes = Like.gql("WHERE post_id = '%s' " %
                                      (str(post_id))).count()
                msg = "You liked the post"

            else:
                msg = "You couldn't like a post twice"
            comments = Comment.gql("WHERE postid = '%s' " % (str(post_id)))

            self.render("permalink.html", post=post,
                        comments=comments, error=msg, numoflikes=numoflikes)
            return
