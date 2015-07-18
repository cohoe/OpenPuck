#!/usr/bin/env python

from hawkeyapi.util import *
from hawkeyapi.CommonDates import *


class Provider(object):
    def __init__(self, index_url):
        url_obj = urlparse(index_url)
        self.server = "%s://%s" % (url_obj.scheme, url_obj.netloc)

    def get_schedule_from_web(self):
        """
        Return a very long string of HTML data from the schedule URL.
        """
        return get_html_from_url(self.urls['schedule'])

    def is_conf_tournament(self, timestamp):
        """
        Return true or false as to if the given timestamp is a conference
        tournament game.
        """
        return (timestamp >= DATE_CONFERENCE_TOURNAMENT_START and
                timestamp < DATE_NATIONAL_TOURNAMENT_START)

    def is_national_tournament(self, timestamp):
        """
        Return true or false as to if the given timestamp is a national
        tournament game.
        """
        return (timestamp >= DATE_NATIONAL_TOURNAMENT_START)

    def is_preseason(self, timestamp):
        """
        Return true of false as to if the given timestamp is a preseason
        game.
        """
        return (timestamp < DATE_SEASON_START)

    def get_normalized_location(self, raw_location):
        """
        Normalize an effectively randomly formatted location string.
        """
        # Make it all uppercase
        n_location = raw_location.upper()

        # Turn slashes into spaces just to make life a bit nicer
        n_location = re.sub(r'[\/\\]', ' ', n_location)

        # Remove special characters
        n_location = re.sub(r'[^\w ]', '', n_location)

        # Remove duplicate spaces
        n_location = re.sub(r'\s+', ' ', n_location)

        # Remove AT
        n_location = re.sub(r'^AT ', '', n_location)

        # Done for now
        return n_location

    def get_normalized_opponent(self, raw_opponent):
        """
        Normalize an effectively randomly formatted opponent string.
        """
        # Make it all uppercase
        n_opponent = raw_opponent.upper()

        # If it's a to be determined, make it so
        if "TBA" in n_opponent or n_opponent == "":
            return "TBA"

        # If there is anything in parenthesis, kill it
        n_opponent = re.sub(r'\((.*)\)', '', n_opponent)

        # Remove special characters
        n_opponent = re.sub(r'[^\w ]', '', n_opponent)

        # Remove duplicate spaces
        n_opponent = re.sub(r'\s+', ' ', n_opponent)
        
        # Remove rankings if that is given
        n_opponent = re.sub(r'^\d+ ', '', n_opponent)
        n_opponent = re.sub(r'NO \d([\/\d]+)?', '', n_opponent)
        n_opponent = n_opponent.strip()

        # If they say the opponent is "at", remove it
        n_opponent = re.sub(r'^AT ', '', n_opponent)
        
        # Same with "vs"
        n_opponent = re.sub(r'^VS ', '', n_opponent)

        # Lastly, strip it up again
        n_opponent = n_opponent.strip()

        # Done for now
        return n_opponent

    def get_json_entry(self, game_id, timestamp, opponent, site,
                       location, links, notes=None):
        """
        Return a JSON entry representing the game.
        """
        game_dict = {
            'gameId': game_id,
            'startTime': timestamp.isoformat(),
            'opponent': opponent,
            'site': site,
            'location': location,
            'isConfTourney': self.is_conf_tournament(timestamp),
            'isNatTourney': self.is_national_tournament(timestamp),
            'isPreSeason': self.is_preseason(timestamp),
            'mediaUrls': links,
            'provider': self.provider_name,
            'notes': notes,
        }

        return dict2json("raw_game", game_dict, True)

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
    
    def get_gameid_from_timestamp(self, timestamp):
        """
        Return a gameID value from a given timestamp.
        Used for teams that do not have their own gameids
        """
        return "%i%i%i%i" % (timestamp.year, timestamp.month, timestamp.day, timestamp.hour)
