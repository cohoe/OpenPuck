#!/usr/bin/env python

import urllib2
import re
import json
from bs4 import BeautifulSoup
from urlparse import urlparse
from datetime import datetime

HTTP_REQUEST_HEADERS = {'User-Agent': 'Mozilla/5.0'}


def get_html_from_url(url):
    """
    Return the HTML contents from a request to a given URL.
    """
    req = urllib2.Request(url, headers=HTTP_REQUEST_HEADERS)
    response = urllib2.urlopen(req)

    return response.read()


def chomp(text):
    """
    Remove newline characters from text.
    """
    return text.rstrip().lstrip()


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


def get_soup_from_html(html):
    """
    Return a soup tree from a given HTML string.
    """
    return BeautifulSoup(html)


def get_combined_timestamp(date_string, date_format, time_string, time_format):
    """
    Return a datetime object representing the local start time of a game.
    """

    date_obj = datetime.strptime(date_string, date_format)
    time_obj = datetime.strptime(time_string, time_format)

    return datetime.combine(date_obj, time_obj.time())
