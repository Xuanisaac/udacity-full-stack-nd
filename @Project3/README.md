## Project Multi User Blog

Multi User Blog is a blogging website that is part of Udaicty Full Stack Developer Nanodegree. The Blog supports general user register, login, authetication, post, edit, delete, like function.

It was built to be deployed on [Google App Engine](https://cloud.google.com/appengine/docs/python/).

[See working example here](https://multi-user-blog-2017.appspot.com).

## Technologies

Language: Python version 2.7

APIs: [NDB Datastore API](https://developers.google.com/appengine/docs/python/ndb/)

Dependencies:

- [webapp2 framework](https://cloud.google.com/appengine/docs/python/tools/webapp2)
- [jinja2 template engine](http://jinja.pocoo.org/)

## Install

In order to install python, please refer to [Python.org](https://www.python.org/downloads/)

To deploy the app yourself, first clone this repo using
```
git clone https://github.com/Xuanisaac/nd_full_stack_multi_user_blog.git
```

And please refer to [Google Cloud Platform](https://cloud.google.com/appengine/docs/python/getting-started/deploying-the-application) to create your own google app engine account and make necessary changes in `app.yaml` and `index.yaml`
