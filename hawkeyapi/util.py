#!/usr/bin/env python

import urllib2
import re
import json
import requests
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


def get_datetime_from_string(string, years=None):
    """
    Return an object from a given date string. Best guess.
    """
    string = string.upper().strip()
    # Dashes mean they dont know the schedule yet. Just do the 1st.
    if "-" in string:
        string = string.split("-")[0].strip()

    # Sub some characters
    if re.search(r'[A-Z]\.[A-Z]\.', string):
        # Remove the dots from things like P.M.
        string = string.replace('.', '')

    # TBA/D
    if "TBA" in string or string == "":
        string = "12:00 AM"
    if "TBD" in string or string == "":
        string = "12:00 AM"
    if "FINAL" in string:
        string = "12:00 AM"
    if "POSTPONED" in string:
        string = "12:00 AM"

    if "NOON" in string:
        string = "12:00 PM"

    # Remove time zone crap
    string = re.sub(r'\(.*\)', '', string)

    # Some of them dont even put the year. Figure it out.
    if re.search(r'[a-zA-Z]{4+}', string):
        if re.search(r'SEP|OCT|NOV|DEC', string):
            string = string + " %i" % years[0]
        else:
            string = string + " %i" % years[1]

    return dateutil.parser.parse(string)

