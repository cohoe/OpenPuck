#!/usr/bin/env python

from Provider import *


class NeulionAdaptiveProvider(Provider):
    def __init__(self, team):
        """
        Constructor
        """
        Provider.__init__(self, team)

        index_url = team.website['index_url']
        self.set_provider_urls(index_url)
        self.provider_name = __name__

    def set_provider_urls(self, index_url):
        """
        Set our URLs so we can reference them later.
        """
        url_obj = urlparse(index_url)
        soup = BeautifulSoup(get_html_from_url(index_url))

        self.urls = {
            'index': index_url,
            'schedule': self.server + soup.find(id='section-menu').find('a', text="Schedule")['href']
        }

    def get_schedule(self, season):
        """
        Return a list of JSON objects of the schedule.
        """
        url = self.get_schedule_url_for_season(season)
        soup = BeautifulSoup(self.get_schedule_from_web())

        # Years
        page_title = soup.find(id='schedule-table').caption.text
        schedule_years = self.get_data_years(page_title)

        games = []
        game_entries = self.get_game_entries(soup)

        for game in game_entries:
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
            # Game ID
            game_id = int(game['schedule-id'])
            # Conference
            conference = self.get_game_conference(game)

            game = ScheduleEntry(game_id, timestamp, opponent, site, location, links, conference, season)
            games.append(game)

        return games

    def get_game_entries(self, soup):
        """
        Return a list of elements containing games. Usually divs or rows.
        """
        schedule_table = soup.find(id="schedule-table")
        results = []
        for row in schedule_table.find_all('tr', class_=['even', 'odd']):
            if "tournament" in row['class']:
                continue

            results.append(row)
        return results

    def get_game_location(self, game):
        """
        Return a normalized string of the games location.
        """
        location_element = game.find('td', class_='location')
        return self.get_normalized_location(location_element.text)

    def get_game_site(self, game):
        """
        Return a normalized string of the games site classification.
        """
        if "home" in game['class']:
            return self.get_normalized_site("home")
        elif "tournament" in game['class']:
            return self.get_normalized_site("neutral")
        else:
            return self.get_normalized_site("away")

    def get_game_opponent(self, game):
        """
        Return a normalized string of the games opponent.
        """
        opponent_element = game.find('td', class_='opponent')
        return self.get_normalized_opponent(opponent_element.text)

    def get_game_media_urls(self, game):
        """
        Locate the media URLs from the details box.
        """
        # @TODO: This needs implemented when data is actually available
        media_urls = {}

        media_element = game.find('td', class_='media')
        for link in media_element.find_all('a'):
            if link.text == "Live Stats":
                media_urls['stats'] = self.server + link['href']

        return media_urls

    def get_game_time(self, game):
        """
        Return a datetime object of the games start time.
        """
        time_string = game.find('td', class_='time').text
        return get_datetime_from_string(time_string)

    def get_game_date(self, game, years):
        """
        Return a datetime object of the games start date.
        """
        date_element = game.find('td', class_='date').div
        date_string = date_element.text.strip().upper()

        return get_datetime_from_string(date_string)

    def get_game_conference(self, game):
        """
        Is this a conference game?
        """
        raw_opponent = game.find('td', class_='opponent').text
        return ("*" in raw_opponent)

    def get_schedule_url_for_season(self, season):
        """
        Return the full URL of the schedule for a given season.
        """
        return "%s&Q_SEASON=%i" % (self.urls['schedule'], season.start_year)
