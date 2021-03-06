#!/usr/bin/env python

from Provider import *


class TemplateProvider(Provider):
    def __init__(self, index_url):
        """
        Constructor
        """
        Provider.__init__(self, index_url)

        self.set_provider_urls(index_url)
        self.provider_name = __name__

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
        soup = get_soup_from_content(self.get_schedule_from_web())

        games = []

        game_entries = self.get_game_entries(soup)

        for game in game_entries:
            # Game ID

            # Location
            location = self.get_game_location(game)
            # Site
            site = self.get_game_site(game)
            # Opponent
            opponent = self.get_game_opponent(game)
            # Links
            links = self.get_game_media_urls(game)
            # Timestamp
            game_time = self.get_game_time(game)
            game_date = self.get_game_date(game)

            game = ScheduleEntry(game_id, game_date, game_time, opponent, site, location, links, season.league, season.id)
            games.append(game)

        return games

    def get_game_entries(self, soup):
        """
        Return a list of elements containing games. Usually divs or rows.
        """

    def get_game_location(self, game):
        """
        Return a normalized string of the games location.
        """
        return self.get_normalized_location(location)

    def get_game_site(self, game):
        """
        Return a normalized string of the games site classification.
        """

    def get_game_opponent(self, game):
        """
        Return a normalized string of the games opponent.
        """
        return self.get_normalized_opponent(opponent)

    def get_game_media_urls(self, game):
        """
        Locate the media URLs from the details box.
        """
        media_urls = {
            'audio': False,
            'video': False,
            'stats': False,
        }

        return media_urls

    def get_game_time(self, game):
        """
        Return a datetime object of the games start time.
        """

        return get_datetime_from_string(time_string)

    def get_game_date(self, game):
        """
        Return a datetime object of the games start date.
        """

        return get_datetime_from_string(date_string)

    @classmethod
    def detect(cls, soup):
        """
        Determine of the URL is handled by this provider.
        :param soup: The site content object to check.
        :return: Boolean of whether this site is mine.
        """
        return 'HELLO'
