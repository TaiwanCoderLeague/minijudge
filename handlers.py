#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp2
from jinja2 import Environment, FileSystemLoader
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras.appengine.users import *
from independent_unit import *

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

        (url, success, msg) = ping_url(url=self.request.get('inputURL'))
        print (url, success, msg)

        self.updateUser(url, success, msg)
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
    #created_time = ndb.StringProperty()
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
        for user in users:
            user.created_time = judgeTime(user.created)
        self.render('dashboard.html', users=users)


