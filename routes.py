#!/usr/bin/python
# -*- coding: utf-8 -*-

import handlers

_routes = [('/', handlers.DashBoard), ('/test', handlers.TestHandler),
           ('/user', handlers.UserHandler), ('/minijudge',
           handlers.MiniJudge), ('/profile/(\d+)',
           handlers.ProfilePage)]
