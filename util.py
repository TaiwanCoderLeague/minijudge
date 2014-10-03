#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Utility functions module

All functions that will be reused all over again should be placed in this module. 
"""

from handlers import *
from google.appengine.api import users


def fixtureUsers():
    data = ['1111', '22222', '333333']
    for d in data:

        u = User.register(uid=d, name=d, site='http://foo%s.appspot.com'
                           % d, is_sucess=False)
        u.put()
        if u:
            print 'fixture %s added' % d


