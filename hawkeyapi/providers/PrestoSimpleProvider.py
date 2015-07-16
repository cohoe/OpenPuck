#!/usr/bin/env python

from Provider import *


class PrestoSimpleProvider(Provider):
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

        sport = url_obj.path.split("/")[2]
        season = DATE_SEASON
        schedule_url = "%s://%s/sports/%s/%s/schedule" % (url_obj.scheme, url_obj.netloc, sport, season)

        self.urls = {
            'index': index_url,
            'schedule': schedule_url,
        }

    def get_schedule(self):
        """
        Return a list of JSON objects of the schedule.
        """
        soup = BeautifulSoup(self.get_schedule_from_web())

        json_games = []

        schedule_years = self.get_schedule_years(soup)

        game_entries = self.get_game_entries(soup)
        for game in game_entries:
            # They do not provide a common location field, so
            # we have to assume it is not there. Sometimes it's given in the
            # notes column but that is not standard.
            location = None
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
            # They don't have game_id's, so lets build one
            game_id = "%i%i%i%i" % (timestamp.year, timestamp.month, timestamp.day, timestamp.hour)

            json_game = self.get_json_entry(game_id, timestamp, opponent, site, location, links)
            json_games.append(json_game)

        return json_games

    def get_game_entries(self, soup):
        """
        Return a list of elements containing games. Usually divs or rows.
        """
        # Skip the first since its always an empty
        games = []
        table_element = soup.find('table', class_='schedule')
        # @TODO: row0 and row1 are the same game. Parse, combine, and return both
        for game in table_element.find_all('tr', class_=['schedule-row0', 'schedule-row1']):
            if game.text.strip() != "":
                games.append(game)

        return games

    def get_game_site(self, game):
        """
        Return a normalized string of the games site classification.
        """
        opponent_element = game.find_all('td')[1]
        if opponent_element.b:
            return self.get_normalized_site("home")
        else:
            return self.get_normalized_site("away")

    def get_game_opponent(self, game):
        """
        Return a normalized string of the games opponent.
        """
        raw_opponent = game.find_all('td')[1].text.strip()
        raw_opponent = re.sub(r'^at ', '', raw_opponent)
        return self.get_normalized_opponent(raw_opponent)

    def get_game_media_urls(self, game):
        """
        Locate the media URLs from the details box.
        """
        media_urls = {
            'audio': False,
            'video': False,
            'stats': False,
        }
        # @TODO: Implement column lookups and something to deal with multirows
        links_element = game.find_all('td')[5]
        for link in links_element.find_all('a'):
            if link.text == "Live stats":
                media_urls['stats'] = self.server + link['href']
            elif link.text == "Video":
                media_urls['video'] = self.server + link['href']
            elif link.text == "Audio":
                media_urls['audio'] = self.server + link['href']

        return media_urls

    def get_game_time(self, game):
        """
        Return a datetime object of the games start time.
        """
        time_string = game.find_all('td')[4].text.strip()

        return get_datetime_from_string(time_string)

    def get_game_date(self, game, years):
        """
        Return a datetime object of the games start date.
        """
        # The field only gives us the day of the month
        date_string = game.find_all('td')[0].text.upper().strip()

        # Figure out which year should be put in
        if re.search(r'SEP|OCT|NOV|DEC', date_string):
            date_string = date_string + " %i" % years[0]
        else:
            date_string = date_string + " %i" % years[1]

        return get_datetime_from_string(date_string)

    def get_schedule_years(self, soup):
        """
        Return two integers representing the years of this schedule
        """
        page_title = soup.title.text
        year_string = re.sub(r'[^\d-]', '', page_title)
        years = year_string.split("-")
        n_years = []
        for year in years:
            if len(year) == 2:
                year = "20" + year
            if len(year) == 4:
                n_years.append(int(year))

        return n_years
