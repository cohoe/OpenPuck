#!/usr/bin/env python

from Provider import *


class StreamlineProvider(Provider):
    def __init__(self, team, season):
        """
        Constructor
        """
        Provider.__init__(self, team, season)

        index_url = team.website
        self.set_provider_urls(index_url)
        self.provider_name = __name__

    def set_provider_urls(self, index_url):
        """
        Set our URLs so we can reference them later.
        """
        self.urls = {
            'index': index_url,
            'schedule': "%s/schedule" % index_url
        }

    def get_schedule(self):
        """
        Return a list of JSON objects of the schedule.
        """
        url = self.get_schedule_url_for_season(self.season)
        soup = get_soup_from_content(get_html_from_url(url))

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
            game_time = self.get_game_time(game)
            game_date = self.get_game_date(game, self.season.years())
            # Game ID
            game_id = self.get_gameid_from_date_time(game_date, game_time)
            # Conference
            conference = self.get_game_conference(game)

            game = ScheduleEntry(game_id, game_date, game_time, opponent, site,
                                 location, links, conference,
                                 self.season.league, self.season.id,
                                 self.team_id, self.is_women)
            games.append(game)

        return games

    def get_game_entries(self, soup):
        """
        Return a list of elements containing games. Usually divs or rows.
        """
        schedule_table = soup.find('table', class_='schedule')
        headers = [header.text.upper().strip() for header in
                   schedule_table.tr.find_all('th')]
        headers = self.get_clean_headers(headers)

        games = []
        for row in schedule_table.find_all('tr'):
            if row.th:
                # It contains headers
                continue
            if "groupstart" in row['class'] or "groupend" in row['class']:
                continue

            game = {}
            for i, cell in enumerate(row.find_all('td')):
                game[headers[i]] = cell

            game['CLASS'] = row['class']
            games.append(game)

        return games

    def get_game_location(self, game):
        """
        Return a normalized string of the games location.
        """
        location = game['LOCATION'].text
        return self.get_normalized_location(location)

    def get_game_site(self, game):
        """
        Return a normalized string of the games site classification.
        """
        if 'shaded' in game['CLASS']:
            return self.get_normalized_site('home')
        else:
            return self.get_normalized_site('away')

    def get_game_opponent(self, game):
        """
        Return a normalized string of the games opponent.
        """
        opponent = game['OPPONENT'].span.text
        return self.get_normalized_opponent(opponent)

    @classmethod
    def get_game_media_urls(cls, game):
        """
        Locate the media URLs from the details box.
        """
        media_urls = {}

        # They don't have any posted :(

        return media_urls

    @classmethod
    def get_game_time(cls, game):
        """
        Return a time object of the games start time.
        """
        time_string = game['TIME'].text

        return get_time_from_string(time_string)

    @classmethod
    def get_game_date(cls, game, years):
        """
        Return a date object of the games start date.
        """
        date_string = game['DATE'].text.upper().strip()

        return get_date_from_string(date_string, years)

    @classmethod
    def get_clean_headers(cls, headers):
        """
        Clean up the headers we get since they have extra crap.
        """
        n_headers = []
        for header in headers:
            # If it has the year its a month header. Replace with date.
            if re.search(r'[0-9]{4}', header):
                header = "DATE"
            # Slashes
            if "/" in header:
                header = header.split("/")[0]
            n_headers.append(header)

        return n_headers

    @classmethod
    def get_game_conference(cls, game):
        """
        Is this a conference game?
        """
        raw_opponent = game['OPPONENT'].text
        return "*" in raw_opponent

    def get_schedule_url_for_season(self, season):
        """
        Return the full URL of the schedule for a given season.
        """
        return "%s/%s/" % (self.urls['schedule'], season.short_id)

    @classmethod
    def detect(cls, soup):
        """
        Determine of the URL is handled by this provider.
        :param soup: The site content object to check.
        :return: Boolean of whether this site is mine.
        """
        if soup.find('div', id='bg-page') is not None:
            return True

        return False
