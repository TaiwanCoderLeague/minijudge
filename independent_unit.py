#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Independent unit module

All utility functions that do not depend on google.appengine.api are included here. (functions depend on google.appengine.api are big headache for testing :( )
"""

import requests
import cgi
import urlparse


def ping_url(url=''):
    """
    Args:
      url (str): comes from self.request.get('anything user keyed in')

    Returns:
      (str, bool, str): a tuple of (parsed_url, is_ping_sucess, message).
    
    Example:
    >>> ping_url("")
    ('', False, 'No url input.')
    
    """

    success = False
    url = urlparse.urlparse(url)

    if url.netloc.endswith('.appspot.com'):

        # url = cgi.escape(url)

        try:
            u = requests.get(url.geturl())

            # see if 200 or 404

            if u.ok:
                msg = \
                    'Congrat! we ping {0} successfully.'.format(url.geturl())
                success = True
            else:
                msg = \
                    'Sorry, 404 not found on {0}.'.format(url.geturl())
        except:
            msg = 'We encounter some tough situation.'
    elif url.netloc:

        msg = \
            'It seems like you didn\'t deploy on GAE, your URL should be like: "foo.appspot.com"'
    elif not url.geturl():

        msg = 'No url input.'
    else:

        msg = 'Invalid URL.'

    return (url.geturl(), success, msg)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
