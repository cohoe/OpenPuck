#!/usr/bin/env python

import urllib2
import re
import json
from bs4 import BeautifulSoup
from urlparse import urlparse
from datetime import datetime
import dateutil.parser

HTTP_REQUEST_HEADERS = {'User-Agent': 'Mozilla/5.0'}


def get_html_from_url(url):
    """
    Return the HTML contents from a request to a given URL.
    """
    req = urllib2.Request(url, headers=HTTP_REQUEST_HEADERS)
    response = urllib2.urlopen(req)

    return response.read()


def dict2json(name, input_dict, debug=False):
    """
    Spit out some JSON from a given dictionary.
    """
    if debug is True:
        return json.dumps({name: input_dict}, sort_keys=True, indent=4,
                          separators=(',', ': '))

    return json.dumps([name, input_dict])


def get_base_from_url(url):
    """
    Return the base server/protocol from a URL
    """
    url_obj = urlparse(url)
    n_url = "%s://%s" % (url_obj.scheme, url_obj.netloc)
    return n_url


def get_combined_timestamp(date, time):
    """
    Return a datetime object representing the local start time of a game.
    """
    return datetime.combine(date, time.time())


def get_list_index(list_, item):
    """
    For a given list, return the position of the given item.
    """
    # This will throw an exception when it's not in there
    return list_.index(item)

def get_datetime_from_string(string):
    """
    Return an object from a given date string. Best guess.
    """
    return dateutil.parser.parse(string)
