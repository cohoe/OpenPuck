#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
from urlparse import urlparse


def get_html_from_url(url):
    """
    Return the HTML contents from a request to a given URL.
    """
    # I have to fake headers because some website filter out bots. Shocking...
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

    @msoucy suggested I don't need this function, but it makes defining
    the HTML parser and any other future requirements in a centralized
    place a lot easier.

    :param content: A very long string of HTML content.
    :return: A BeautifulSoup object.
    """
    return BeautifulSoup(content, "lxml")
