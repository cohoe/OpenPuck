#!/usr/bin/env python

from Provider import *


class NeulionClassicProvider(Provider):
    def __init__(self, team):
        """
        Constructor
        """
        Provider.__init__(self, team)

        index_url = team.website
        self.set_provider_urls(index_url)
        self.provider_name = __name__

    def set_provider_urls(self, index_url):
        """
        Set our URLs so we can reference them later.
        """
        url_obj = urlparse(index_url)
        soup = BeautifulSoup(get_html_from_url(index_url))

        sched_element = soup.find(id='section-menu').find('a', text="SCHEDULE")
        self.urls = {
            'index': index_url,
            'schedule': self.server + sched_element['href']
        }

    def get_schedule(self, season):
        """
        Return a list of JSON objects of the schedule.
        """
        url = self.get_schedule_url_for_season(season)
        soup = BeautifulSoup(get_html_from_url(url))

        game_entries = self.get_game_entries(soup)
        games = []

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
            game_date = self.get_game_date(game, season.years())
            game_time = self.get_game_time(game)
            timestamp = get_combined_timestamp(game_date, game_time)
            # Game ID
            game_id = self.get_gameid_from_timestamp(timestamp)
            # Conference
            conference = self.get_game_conference(game)

            game = ScheduleEntry(game_id, game_date, game_time, opponent, site,
                                 location, links, conference, season)
            games.append(game)

        return games

    def get_game_entries(self, soup):
        """
        Return a list of elements containing games. Usually divs or rows.
        """
        schedule_table = soup.find(id="schedule-table")
        headers = [header.text.upper().strip() for header in schedule_table.find_all('th')]
        results = []
        for row in schedule_table.find_all('tr'):
            game = {}
            for i, cell in enumerate(row.find_all('td')):
                game[headers[i]] = cell

            if "tournament-head" in row['class'] or "tournament-end" in row['class']:
                continue

            game['CLASS'] = row['class']
            results.append(game)
        return results

    def get_game_location(self, game):
        """
        Return a normalized string of the games location.
        """
        return self.get_normalized_location(game['LOCATION'].text)

    def get_game_site(self, game):
        """
        Return a normalized string of the games site classification.
        """
        if "home" in game['CLASS']:
            return self.get_normalized_site("home")
        elif "tournament" in game['CLASS']:
            return self.get_normalized_site("neutral")
        else:
            return self.get_normalized_site("away")

    def get_game_opponent(self, game):
        """
        Return a normalized string of the games opponent.
        """
        return self.get_normalized_opponent(game['OPPONENT'].text)

    def get_game_media_urls(self, game):
        """
        Locate the media URLs from the details box.
        """
        media_urls = {}

        # @TODO: This needs implemented when data is actually available

        return media_urls

    def get_game_time(self, game):
        """
        Return a time object of the games start time.
        """
        time_header = ""
        for header in game.keys():
            if "TIME" in header:
                time_header = header
                break
        return get_time_from_string(game[time_header].text)

    def get_game_date(self, game, years):
        """
        Return a date object of the games start date.
        """
        date_string = game['DATE'].text.strip().upper()
        return get_date_from_string(date_string, years)

    def get_game_conference(self, game):
        """
        Is this a conference game?
        """
        raw_opponent = game['OPPONENT'].text.strip()
        return ("*" in raw_opponent)

    def get_schedule_url_for_season(self, season):
        """
        Return the full URL of the schedule for a given season.
        """
        return "%s&Q_SEASON=%i" % (self.urls['schedule'], season.start_year)
