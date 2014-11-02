#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp2
from jinja2 import Environment, FileSystemLoader
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras.appengine.users import *
from independent_unit import *
from datetime import datetime

# don't modify the existing element in this list

problem_sets = [
    'helloworld',
    'rot13',
    'signup',
    'blog',
    'registration',
    'login',
    'logout',
    'json',
    ]


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
        self.render('minijudge.html', nickname=self.nickname(),
                    problem_sets=problem_sets)

    def post(self):

        pb_set = self.request.get('pb_set')

        (url, success, msg) = ping_url(url=self.request.get('inputURL'))
        print (url, success, msg)

        if pb_set in problem_sets:
            if pb_set == problem_sets[0]:
                self.updateUser(url, success, msg)
            else:
                self.updateSubmission(pb_set=pb_set, url=url,
                        is_success=success, msg=msg)

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

    def updateSubmission(
        self,
        pb_set='',
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
                q2 = \
                    ndb.gql('SELECT * FROM Submissions WHERE uid = :1 and pb_set = :2'
                            , uid, pb_set)
                s = q2.get()
                if s:
                    s.url = url
                    s.is_success = is_success
                    s.msg = msg
                    s.updated = datetime.utcnow()
                    s.put()
                else:
                    submission = Submissions(
                        uid=uid,
                        name=u.name,
                        pb_set=pb_set,
                        url=url,
                        is_success=is_success,
                        msg=msg,
                        updated=datetime.utcnow(),
                        )
                    submission.put()
            else:

                # in case the user not exist, use current url to register one.

                new_u = User.register(uid=uid, name=user.nickname(),
                        site=url, is_success=is_success, msg=msg)
                new_u.put()


class User(ndb.Model):

    uid = ndb.StringProperty(required=True)
    name = ndb.StringProperty()

    # Root site

    site = ndb.StringProperty()
    is_success = ndb.BooleanProperty()

    # the message that minijudge said

    msg = ndb.StringProperty()

    created = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid)

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


class Submissions(ndb.Model):

    uid = ndb.StringProperty(required=True)
    name = ndb.StringProperty()
    pb_set = ndb.StringProperty(required=True)
    url = ndb.StringProperty()
    is_success = ndb.BooleanProperty()
    msg = ndb.StringProperty()
    updated = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_all(cls):
        return cls.query().order(-cls.updated)


class DashBoard(BaseHandler):

    def get(self):
        users = User.query_all()
        submissions = Submissions.query_all()
        self.render('dashboard.html', users=users,
                    submissions=submissions)


class ProfilePage(BaseHandler):

    def get(self, uid):

        users = ndb.gql('SELECT * FROM User WHERE uid = :1', uid)
        u = users.get()
        submissions = Submissions.query(Submissions.uid == uid)
        if u:
            self.render('profile.html', user=u, submissions=submissions)
        else:
            self.redirect('/')


