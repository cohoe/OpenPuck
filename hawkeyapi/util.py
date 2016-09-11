#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
from urlparse import urlparse


def get_html_from_url(url):
    """
    Return the HTML contents from a request to a given URL.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()

    return r.text


def get_base_from_url(url):
    """
    Return the base server/protocol from a URL
    """
    url_obj = urlparse(url)
    n_url = "%s://%s" % (url_obj.scheme, url_obj.netloc)
    return n_url


def get_soup_from_content(content):
    """
    Return a BeautifulSoup object for given HTML content.
    :param content: A very long string of HTML content.
    :return: A BeautifulSoup object.
    """
    return BeautifulSoup(content, "lxml")
