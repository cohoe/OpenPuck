#!/usr/bin/env python

import inspect
import re
import dateutil.parser
import hawkeyapi.providers
from hawkeyapi.util import get_soup_from_content, get_html_from_url
from datetime import datetime


def get_date_from_string(string, years):
    """
    Return a best-guess date object from given string.
    """
    string = string.upper().strip()

    # If theres a dash in the date, it likely means a range. We're only
    # going to take the first one.
    if "-" in string:
        string = string.split("-")[0].strip()

    # Cut out any () extra crap
    string = re.sub(r'\((.*)\)', '', string)

    if re.search(r'[a-zA-Z]{3,}', string):
        if re.search(r'SEP|OCT|NOV|DEC|JAN|FEB|MAR', string):
            string = string + " %i" % years[0]
        else:
            string = string + " %i" % years[1]

    return dateutil.parser.parse(string).date()


def get_time_from_string(string):
    """
    Return a best-guess time object from the given string.
    """
    string = string.upper().strip()

    # Too be <x>
    # @TODO: This might need some work later on. Midnight games are
    # not likely but could happen.
    if re.search(r'TBA|TBD|FINAL|POSTPONED', string):
        return datetime.time(0, 0)

    # Deal with results
    if re.search(r'[WLT]', string):
        return datetime.time(0, 0)

    # Frak you Robert Morris
    if "NOON" in string:
        return datetime.time(12, 0)

    # Remove extra characters from the time (Thanks
    # MSU for putting a random ` in there...)
    string = re.sub(r'[^a-zA-Z0-9\:]', '', string)

    # Sometimes they put the host or local time zone in there too.
    string = re.sub(r'\(.*\)', '', string)

    return dateutil.parser.parse(string).time()


def get_list_of_providers():
    """
    Return a list of all of the supported Provider objects.
    :return: list of HawkeyApi.Provider's.
    """
    providers = []
    for name, obj in inspect.getmembers(hawkeyapi.providers):
        if inspect.isclass(obj):
            providers.append(obj)

    return providers


def get_provider_for_url(url):
    """
    Find the provider to use for a given URL.
    :param url: The URL to poke at.
    :return: A HawkeyApi.Provider object or None.
    """
    site_content = get_soup_from_content(get_html_from_url(url))

    for provider in get_list_of_providers():
        if provider.detect(site_content) is True:
            return provider
