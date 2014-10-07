#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from independent_unit import *


class TestPingUrl(unittest.TestCase):

    def setUp(self):
        pass

    def test_emptyUrl(self):
        url = ''
        self.assertEqual(ping_url(url), ('', False, 'No url input.'))

    def test_validUrl(self):
        url = 'http://pointlesstire.appspot.com'
        self.assertEqual(ping_url(url),
                         ('http://pointlesstire.appspot.com', True,
                         'Congrat! we ping http://pointlesstire.appspot.com successfully.'
                         ))

    def test_nonsenseUrl(self):
        url = 'avada kedavra'
        self.assertEqual(ping_url(url), ('avada kedavra', False,
                         'Invalid URL.'))

    def test_nonAppspotUrl(self):
        url = 'http://google.com'
        self.assertEqual(ping_url(url), ('http://google.com', False,
                         'It seems like you didn\'t deploy on GAE, your URL should be like: "foo.appspot.com"'
                         ))


# if __name__ == '__main__':
#    unittest.main()

suite = unittest.TestLoader().loadTestsFromTestCase(TestPingUrl)
unittest.TextTestRunner(verbosity=2).run(suite)
