#!/usr/bin/env python

from Provider import *


class SidearmAdaptiveProvider(Provider):
    def __init__(self, index_url):
        """
        Constructor
        """
        Provider.__init__(self, index_url)

        # Set up the URL information for this provider
        self.set_provider_urls(index_url)
        self.provider_name = __name__

    def set_provider_urls(self, index_url):
        """
        Set our URLs so we can reference them later.
        """
        url_obj = urlparse(index_url)

        self.urls = {
            'index': index_url,
            'schedule': "%s://%s/schedule.aspx?%s" % (url_obj.scheme, url_obj.netloc, url_obj.query),
        }

    def get_schedule(self):
        """
        Return a list of JSON objects of the schedule.
        """
        soup = BeautifulSoup(self.get_schedule_from_web())

        # Years
        page_title = soup.find('div', class_='page_title').text
        schedule_years = self.get_data_years(page_title)

        games = []
        game_entries = self.get_game_entries(soup)

        for game in game_entries:
            # Game ID
            game_id = game['id'].split('_')[-1]
            # Location
            location = self.get_game_location(game)
            # Site
            site = self.get_game_site(game)
            # Opponent
            opponent = self.get_game_opponent(game)
            # Links
            links = self.get_game_media_urls(game)
            # Timestamp
            game_date = self.get_game_date(game, schedule_years)
            game_time = self.get_game_time(game)
            timestamp = get_combined_timestamp(game_date, game_time)

            game = ScheduleEntry(game_id, timestamp, opponent, site, location, links)
            games.append(game)

        return games

    def get_game_entries(self, soup):
        """
        Return a list of elements containing games. Usually divs or rows.
        """
        return soup.find_all('div', class_='schedule_game')

    def get_game_location(self, game):
        """
        Return a normalized string of the games location.
        """
        facility_element = game.find('div', class_='schedule_game_facility')
        location_element = game.find('div', class_='schedule_game_location')
        facility = ""
        if facility_element:
            facility = self.get_normalized_location(facility_element.text)
        location = self.get_normalized_location(location_element.text)
        location = ' '.join([facility, location])
        location = location.lstrip()
        return location

    def get_game_site(self, game):
        """
        Return a normalized string of the games site
        classification (home, away, neutral)
        """
        parent_class = game['class'][1:2][0]
        if parent_class == "" or not parent_class:
            parent_class = "home"

        return self.get_normalized_site(parent_class)

    def get_game_opponent(self, game):
        """
        Return a normalized string of the games opponent.
        """
        site = self.get_game_site(game)

        opponent_element = game.find('div', class_='schedule_game_opponent_name')
        opponent = opponent_element.text

        return self.get_normalized_opponent(opponent)

    def get_game_media_urls(self, game):
        """
        Return a normalized dictionary of media URLs.
        """
        media_urls = {}

        media_element = game.find('div', class_='schedule_game_multimedia_links')
        if not media_element:
            return media_urls

        link_elements = media_element.find_all('a', class_='schedule_game_media_link')
        for link in link_elements:
            link_text = link.text.upper()
            if "STATS" in link_text:
                media_urls['stats'] = link['href']
            if "AUDIO" in link_text:
                media_urls['audio'] = link['href']
            if "VIDEO" in link_text:
                media_urls['video'] = link['href']

        return media_urls

    def get_game_date(self, game, years):
        """
        Return a datetime object of the games start time. Note that it will
        have no time so it needs to be paired with a game_time object.
        """
        date_string = game.find('div', class_='schedule_game_opponent_date').text.upper().strip()

        return get_datetime_from_string(date_string, years)

    def get_game_time(self, game):
        """
        Return a datetime object of the games start time. Note that it will
        have todays date so it needs to be combined with a game_date
        object.
        """
        time_string = game.find('div', class_='schedule_game_opponent_time').text.strip()

        return get_datetime_from_string(time_string)
