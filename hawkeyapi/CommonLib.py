#!/usr/bin/env python

import urllib2
import re
import json
from urlparse import urlparse

HTTP_REQUEST_HEADERS = { 'User-Agent': 'Mozilla/5.0' }

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

def normalize_location(location):
    """
    Normalize an effectively randomly formatted location string.
    """
    # Make it all uppercase
    n_location = location.upper()

    # Remove special characters
    n_location = re.sub(r'[^\w ]', '', n_location)

    # Remove duplicate spaces
    n_location = re.sub(r'\s+', ' ', n_location)

    # Done for now
    return n_location

def dict2json(name, input_dict, debug=False):
    """
    Spit out some JSON from a given dictionary.
    """
    if debug is True:
        return json.dumps({name: input_dict}, sort_keys = True, indent=4, separators=(',', ': '))
    return json.dumps([name, input_dict])

def get_base_from_url(url):
    """
    Return the base server/protocol from a URL
    """
    url_obj = urlparse(url)
    n_url = "%s://%s" % (url_obj.scheme, url_obj.netloc)
    return n_url
