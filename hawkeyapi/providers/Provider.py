#!/usr/bin/env python

from hawkeyapi.util import *
from hawkeyapi.providers.util import *
from hawkeyapi.objects import *
# ^^ Contrary to PyCharm's suggestion, that import statement is needed.


class Provider(object):
    def __init__(self, team, season):
        url_obj = urlparse(team.website)
        self.server = "%s://%s" % (url_obj.scheme, url_obj.netloc)
        self.team_id = team.id
        self.is_women = team.is_women
        self.season = season

    def get_schedule_from_web(self):
        """
        Return a very long string of HTML data from the schedule URL.
        """
        return get_html_from_url(self.urls['schedule'])

    def get_normalized_location(self, raw_location):
        """
        Normalize an effectively randomly formatted location string.
        """
        # Make it all uppercase
        n_location = raw_location.upper()

        # Turn slashes into spaces just to make life a bit nicer
        n_location = re.sub(r'[\/\\]', ' ', n_location)

        # Remove special characters
        n_location = re.sub(r'[^\w\- ]', '', n_location)

        # Remove duplicate spaces
        n_location = re.sub(r'\s+', ' ', n_location)

        # Remove AT
        n_location = re.sub(r'^AT ', '', n_location)

        if not n_location or n_location == "":
            return None

        # Done for now
        return n_location

    def get_normalized_opponent(self, raw_opponent):
        """
        Normalize an effectively randomly formatted opponent string.
        """
        # Make it all uppercase and remove extra crap
        n_opponent = raw_opponent.upper().strip()

        # If it's a to be determined, make it so
        if "TBA" in n_opponent or n_opponent == "":
            return None

        # If there is anything in parenthesis, kill it
        n_opponent = re.sub(r'\((.*?)\)', '', n_opponent)

        # Remove anything after an @
        n_opponent = re.sub(r'@ (.*)$', '', n_opponent)

        # Some special words
        # This regex is only going to get longer as schools put stupid crap
        # in the schedule.
        n_opponent = re.sub(r'GAME \d|(SEMI)?FINAL(S)?|CHAMPIONSHIP( GAME)?|NATIONAL QUARTERFINAL', '', n_opponent)
        n_opponent = re.sub(r'FIRST ROUND GAME \w+|QUARTER|SEMIS AND', '', n_opponent)

        # Remove special characters
        n_opponent = re.sub(r'[^\w ]', '', n_opponent)

        # Remove duplicate spaces
        n_opponent = re.sub(r'\s+', ' ', n_opponent)
        
        # Remove rankings if that is given
        n_opponent = re.sub(r'NO \d([\/\dRV]+)?', '', n_opponent)
        n_opponent = re.sub(r'\d+ ', '', n_opponent)
        n_opponent = n_opponent.strip()

        # If they say the opponent is "at", remove it
        n_opponent = re.sub(r'^AT ', '', n_opponent)
        
        # Same with "vs"
        n_opponent = re.sub(r'^VS ', '', n_opponent)

        # Maybe they included a special site
        n_opponent = re.sub(r'AT (.*) ARENA', '', n_opponent)

        # Lastly, strip it up again
        n_opponent = n_opponent.strip()

        if not n_opponent or n_opponent == "":
            return None

        # Done
        return n_opponent

    def get_normalized_site(self, raw_site):
        """
        Return a normalized word indiciating the site of the game.
        """
        if "home" in raw_site:
            return "home"
        elif "away" in raw_site:
            return "away"
        elif "neutral" in raw_site:
            return "neutral"
        else:
            return "UNKNOWN"
    
    def get_gameid_from_date_time(self, i_date, i_time):
        """
        Return a gameID value from a given date and time.
        Used for teams that do not have their own gameids
        """
        return "%i%i%i%i" % (i_date.year, i_date.month, i_date.day, i_time.hour)

    def get_data_years(self, string):
        """
        Return two integers representing the years of a data set from
        a string (usually the title).
        """
        year_string = re.sub(r'[^\d-]', '', string)
        years = year_string.split("-")
        n_years = []
        for year in years:
            if len(year) == 2:
                year = "20" + year
            if len(year) == 4:
                n_years.append(int(year))

        return n_years

    def get_id_from_string(self, string):
        """
        Return an integer ID from a given string by striping out
        all non-number characters.
        """
        return int(re.sub(r'[^\d]', '', string))

    @classmethod
    def get_name(cls):
        return str(cls).split('.')[-1].replace("'>", "")
