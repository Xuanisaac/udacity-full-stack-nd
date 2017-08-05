from bloghandler import BlogHandler
from models.user import User
from models.post import Post
from models.like import Like
from models.comment import Comment
from helper import *
from google.appengine.ext import db


class EditComment(BlogHandler):
    def get(self, comment_id):
        self.redirect('/blog')
        return

    def post(self, comment_id):

        if not self.user:
            self.redirect('/blog')
            return

        content = self.request.get('comment_content')
        post_id = self.request.get('post_id')
        post = self.find_post_from_db(post_id)

        comment_id = int(comment_id)
        key = db.Key.from_path('Comment', int(comment_id))
        comment = db.get(key)
        author = self.get_user_name()

        if comment.author != author:
            msg = "Oops, you are not the author of this post"
            self.render('login-form.html', error=msg)
            return

        if not comment:
            self.error(404)
            return
        if not post:
            self.error(404)
            return
        if not content:
            msg = "Comment cannot be empty"
            comcontent = comment.content
            self.render("editcomment.html", post=post, numoflikes=0,
                        comment_ins=comment, content=comcontent, error=msg)
            return

        comment.content = content
        comment.put()
        self.redirect('/blog/%s' % (str(post_id)))
        return
