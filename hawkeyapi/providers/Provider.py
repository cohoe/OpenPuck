#!/usr/bin/env python

from hawkeyapi.util import *
from hawkeyapi.CommonDates import *


class Provider(object):
    def __init__(self):
        pass

    def get_schedule(self):
        """
        This function should return a list of JSON objects
        representing a complete schedule.
        """
        raise NotImplementedError("This function is required for a provider.")

    def get_timestamp(self):
        """
        This function should return a datetime object representing the start
        time of a game.
        """
        raise NotImplementedError("This function is required for a provider.")

    def get_normalized_site(self, raw_site):
        """
        Return a normalized word indiciating the site of the game.
        * home
        * away
        * neutral
        """
        raise NotImplementedError("This function is required for a provider.")

    def get_schedule_from_web(self):
        """
        Return a very long string of HTML data from the schedule URL.
        """
        html = get_html_from_url(self.urls['schedule'])
        return html

    def is_conf_tournament(self, timestamp):
        """
        Return true or false as to if the given timestamp is a conference
        tournament game.
        """
        if (timestamp >= DATE_CONFERENCE_TOURNAMENT_START and
           timestamp < DATE_NATIONAL_TOURNAMENT_START):
            return True

        return False

    def is_national_tournament(self, timestamp):
        """
        Return true or false as to if the given timestamp is a national
        tournament game.
        """
        if timestamp >= DATE_NATIONAL_TOURNAMENT_START:
            return True

        return False

    def is_preseason(self, timestamp):
        """
        Return true of false as to if the given timestamp is a preseason
        game.
        """
        if timestamp < DATE_SEASON_START:
            return True

        return False

    def get_normalized_location(self, raw_location):
        """
        Normalize an effectively randomly formatted location string.
        """
        # Make it all uppercase
        n_location = raw_location.upper()

        # Remove special characters
        n_location = re.sub(r'[^\w ]', '', n_location)

        # Remove duplicate spaces
        n_location = re.sub(r'\s+', ' ', n_location)

        # Done for now
        return n_location

    def get_normalized_opponent(self, raw_opponent):
        """
        Normalize an effectively randomly formatted opponent string.
        """
        # Make it all uppercase
        n_opponent = raw_opponent.upper()

        # If it's a to be determined, make it so
        if "TBA" in n_opponent:
            return "TBA"

        # Remove special characters
        n_opponent = re.sub(r'[^\w ]', '', n_opponent)

        # Remove duplicate spaces
        n_opponent = re.sub(r'\s+', ' ', n_opponent)
        
        # Remove leading numbers from ranked teams
        n_opponent = re.sub(r'^\d+ ', '', n_opponent)

        # Done for now
        return n_opponent

    def get_date_range(self, date_string):
        """
        Return the month, year, and start/end dates for a date range.
        """
        if "-" not in date_string:
            return date_string

        month, days, year = date_string.split('/')
        start_day, end_day = days.split('-')
        start_day = int(start_day)
        end_day = int(end_day)
        month = int(month)
        year = int(year)

        end_day += 1

        return month, year, start_day, end_day

    def get_html_from_url(self, url):
        """
        Return the HTML contents from a request to a given URL.
        """
        req = urllib2.Request(url, headers=HTTP_REQUEST_HEADERS)
        response = urllib2.urlopen(req)

        return response.read()

    def dict2json(self, name, input_dict, debug=False):
        """
        Spit out some JSON from a given dictionary.
        """
        if debug is True:
            return json.dumps({name: input_dict}, sort_keys=True, indent=4,
                              separators=(',', ': '))

        return json.dumps([name, input_dict])

    def get_base_from_url(self, url):
        """
        Return the base server/protocol from a URL
        """
        url_obj = urlparse(url)
        n_url = "%s://%s" % (url_obj.scheme, url_obj.netloc)
        return n_url

    def get_soup_from_html(self, html):
        """
        Return a soup tree from a given HTML string.
        """
        return BeautifulSoup(html)

    def get_combined_timestamp(self, date_string, date_format, time_string, time_format):
        """
        Return a datetime object representing the local start time of a game.
        """

        date_obj = datetime.strptime(date_string, date_format)
        time_obj = datetime.strptime(time_string, time_format)

        return datetime.combine(date_obj, time_obj.time())
