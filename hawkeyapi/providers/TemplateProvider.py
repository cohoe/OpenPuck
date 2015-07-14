#!/usr/bin/env python

from Provider import *


class TemplateProvider(Provider):
    def __init__(self, index_url):
        """
        Constructor
        """
        Provider.__init__(self)

        self.set_provider_urls(index_url)

    def set_provider_urls(self, index_url):
        """
        Set our URLs so we can reference them later.
        """
        url_obj = urlparse(index_url)

        self.urls = {
            'index': index_url,
        }

    def get_schedule(self):
        """
        Return a list of JSON objects of the schedule.
        """
        html = self.get_schedule_from_web()
        soup = BeautifulSoup(html)

        json_games = []

        game_entries = self.get_game_entries(soup)

        for game in game_entries:
            # Game ID
            # Location
            # Site
            # Opponent
            # Links
            # Timestamp

            json_game = self.get_json_entry(game_id, timestamp, opponent, site, location, links)
            json_games.append(json_game)

        return json_games

    def get_game_entries(self, soup):
        """
        Return a list of elements containing games. Usually divs or rows.
        """

    def get_game_location(self, game):
        """
        Return a normalized string of the games location.
        """

    def get_game_site(self, game):
        """
        Return a normalized string of the games site classification.
        """

    def get_game_opponent(self, game):
        """
        Return a normalized string of the games opponent.
        """

    def get_game_media_urls(self, game):
        """
        Locate the media URLs from the details box.
        """

    def get_game_time(self, game):
        """
        Return a datetime object of the games start time.
        """

    def get_game_date(self, game):
        """
        Return a datetime object of the games start date.
        """

    def get_game_timestamp(self, game):
        """
        Return a datetime object representing the start time of the game.
        """

        return datetime.combine(game_date, game_time.time())
