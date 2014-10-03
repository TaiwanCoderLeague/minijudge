#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp2
from jinja2 import Environment, FileSystemLoader
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras.appengine.users import *
import requests, cgi, urlparse


class MainHandler(webapp2.RequestHandler):

    def get(self):

        self.response.out.write('hello world')


class BaseHandler(webapp2.RequestHandler):

    def render(self, filename, **template_values):
        jinja_env = Environment(loader=FileSystemLoader('templates'))
        template = jinja_env.get_template(filename)
        self.response.out.write(template.render(template_values))

    def nickname(self):
        user = users.get_current_user()
        if user:
            return user.nickname()
        else:
            return 'fella'


class TestHandler(BaseHandler):

    def get(self):
        self.render('test.html')


class UserHandler(BaseHandler):

    def get(self):
        user = users.get_current_user()

        if user:
            self.render('user.html', msg='Hello, ' + user.nickname())
        else:
            self.redirect(users.create_login_url(self.request.uri))


class MiniJudge(BaseHandler):

    @login_required
    def get(self):
        self.render('minijudge.html', nickname=self.nickname())

    def post(self):

        success = False
        url = urlparse.urlparse(self.request.get('inputURL'))

        if url.netloc.endswith(".appspot.com"):
            #url = cgi.escape(url)
            print url
            try:
                u = requests.get(url.geturl())

                # see if 200 or 404

                if u.ok:
                    msg = 'Congrat! we ping {0} successfully.'.format(url.geturl())
                    success = True
                else:
                    msg = 'Sorry, 404 not found on {0}.'.format(url.geturl())
            except:
                msg = 'We encounter some tough situation.'

        elif url.netloc:
            msg = "It seems like you didn't deploy on GAE, your URL should be like: \"foo.appspot.com\""

        elif not url.geturl():
            msg = 'No url input.'

        else:
            msg = "Invalid URL."

        

        self.updateUser(url.geturl(), success, msg)
        self.render('minijudge.html', msg=msg, nickname=self.nickname())

        if success:
            print 'url ping success'
            self.redirect('/')

    def updateUser(
        self,
        url='',
        is_success=False,
        msg='',
        ):

        user = users.get_current_user()
        if user:
            uid = user.user_id()
            q = ndb.gql('SELECT * FROM User WHERE uid = :1', uid)
            u = q.get()
            if u:
                print 'This user already stored in db, here it is %s' \
                    % u
                u.site = url
                u.is_success = is_success
                u.msg = msg
                u.put()
            else:
                print 'This user is not yet in db, storing now'
                new_u = User.register(uid=uid, name=user.nickname(),
                        site=url, is_success=is_success, msg=msg)
                new_u.put()


class User(ndb.Model):

    uid = ndb.StringProperty(required=True)
    name = ndb.StringProperty()
    site = ndb.StringProperty()
    is_success = ndb.BooleanProperty()
    msg = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=users_key())

#    @classmethod
#    def by_name(cls, name):
#        u = User.all().filter('name =', name).get()
#        return u
#

    @classmethod
    def register(
        cls,
        uid,
        name='',
        site='',
        is_success=False,
        msg='',
        ):

        return User(uid=uid, name=name, site=site,
                    is_success=is_success, msg=msg)

    @classmethod
    def query_all(cls):
        return cls.query().order(-cls.created)


#
#    @classmethod
#    def login(cls, name, pw):
#        u = cls.by_name(name)
#        if u and valid_pw(name, pw, u.pw_hash):
#            return u

#        u = User.by_name(self.username)
#        if u:
#            msg = 'The user already exists.'
#            self.write('signup.html', user_error=msg)
#        else:
#            u = User.register(self.username, self.password, self.email)
#        u.put()
#
#        self.login(u)
#        self.redirect('/welcome')

class DashBoard(BaseHandler):

    def get(self):
        users = User.query_all()
        self.render('dashboard.html', users=users)


