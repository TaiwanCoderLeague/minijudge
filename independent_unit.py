#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Independent unit module

All utility functions that do not depend on google.appengine.api are included here. (functions depend on google.appengine.api are big headache for testing :( )
"""
import datetime
import requests
import cgi
import urlparse

def judgeTime(created):
    #declare variables
    host_current_time = datetime.datetime.now().isoformat()
    created = created.isoformat()

    createdYear = int(created[:4])#2014 year
    createdMon = int(created[5:7])#10 mon
    createdDay = int(created[8:10])#08 day
    createdHour = int(created[11:13])#14 hr
    createdMin = int(created[14:16])#58 min
    createdSec = int(created[17:19])#46s

    hostYear = int(host_current_time[:4])#2014 year
    hostMon = int(host_current_time[5:7])#10 mon
    hostDay = int(host_current_time[8:10])#08 day
    hostHour = int(host_current_time[11:13])#14 hr
    hostMin = int(host_current_time[14:16])#58 min
    hostSec = int(host_current_time[17:19])#46 s

    createdTIME = 'Error'
    #Judege
    if hostYear > createdYear:
        if hostYear - createdYear > 1:
            createdTIME = '%d years ago' %(hostYear - createdYear)
        else:
            createdTIME = '%d year ago' %(hostYear - createdYear)
        return  createdTIME
    elif hostMon > createdMon :
        if hostMon - createdMon > 1:
            createdTIME = '%d months ago' %(hostMon - createdMon)
        else:
            createdTIME = '%d month ago' %(hostMon - createdMon)
        return  createdTIME
    elif hostDay > createdDay :
        if hostDay - createdDay > 1:
            createdTIME = '%d days ago' %(hostDay - createdDay)
        else:
            createdTIME = '%d day ago' %(hostDay - createdDay)
        return  createdTIME
    elif hostHour > createdHour :
        if hostHour - createdHour > 1:
            createdTIME = '%d hours ago' %(hostHour - createdHour)
        else:
            createdTIME = '%d hour ago' %(hostHour - createdHour)
        return  createdTIME
    elif hostMin > createdMin :
        if hostMin - createdMin > 1:
            createdTIME = '%d miniutes ago' %(hostMin - createdMin)
        else:
            createdTIME = '%d miniute ago' %(hostMin - createdMin)
        return  createdTIME
    elif hostSec > createdSec :
        if hostSec - createdSec > 1:
            createdTIME = '%d seconds ago' %(hostSec - createdSec)
        else:
            createdTIME = '%d second ago' %(hostSec - createdSec)
        return  createdTIME
    else:
        return createdTIME


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
