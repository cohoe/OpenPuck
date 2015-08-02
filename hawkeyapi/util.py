#!/usr/bin/env python

import re
import json
import requests
from bs4 import BeautifulSoup
from urlparse import urlparse
import datetime
import dateutil.parser
import requests


def get_html_from_url(url):
    """
    Return the HTML contents from a request to a given URL.
    """
    r = requests.get(url)
    r.raise_for_status()

    return r.text


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
    return datetime.datetime.combine(date, time)


def get_date_from_string(string, years):
    """
    Return a best-guess date object from given string.
    """
    string = string.upper().strip()

    # If theres a dash in the date, it likely means a range. We're only
    # going to take the first one.
    if "-" in string:
        string = string.split("-")[0].strip()

    if re.search(r'[a-zA-Z]{3,}', string):
        if re.search(r'SEP|OCT|NOV|DEC', string):
            string = string + " %i" % years[0]
        else:
            string = string + " %i" % years[1]

    return dateutil.parser.parse(string).date()

def get_time_from_string(string):
    """
    Return a best-guess time object from the given string.
    """
    string = string.upper().strip()

    # Remove the dots from the time (such as "P.M.")
    string = string.replace('.', '')

    # Deal with results
    if re.search(r'[WL]', string):
        # @TODO This might be becoming None in the future.
        return datetime.time(0, 0)
    
    # Too be <x>
    if re.search(r'TBA|TBD|FINAL|POSTPONED', string):
        # @TODO Same thing here
        return datetime.time(0, 0)

    # Frak you Robert Morris
    if "NOON" in string:
        return datetime.time(12, 0)

    # Sometimes they put the host or local time zone in there too.
    string = re.sub(r'\(.*\)', '', string)

    return dateutil.parser.parse(string).time()
