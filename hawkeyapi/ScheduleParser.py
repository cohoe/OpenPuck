#!/usr/bin/env python

from CommonLib import *

def parse2json(url):
    """
    Take a schedule URL and return a JSON schedule.
    """
    html_content = get_html_from_url(url)

    # Pick parser
    if "sidearm" in html_content:
        from providers import Sidearm
        games = Sidearm.parse_schedule_to_json(url, html_content)
    else:
        print "Data provider could not be located."

    return games
