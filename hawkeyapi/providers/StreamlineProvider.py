#!/usr/bin/env python

from Provider import *


class StreamlineProvider(Provider):
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
            'schedule': "%s/schedule/%s" % (index_url, DATE_SEASON)
        }

    def get_schedule(self):
        """
        Return a list of JSON objects of the schedule.
        """
        soup = BeautifulSoup(self.get_schedule_from_web())

        json_games = []

        game_entries = self.get_game_entries(soup)
        schedule_years = self.get_schedule_years(soup)

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
            game_date = self.get_game_date(game, schedule_years)
            timestamp = get_combined_timestamp(game_date, game_time)
            # Game ID
            game_id = self.get_gameid_from_timestamp(timestamp)

            json_game = self.get_json_entry(game_id, timestamp, opponent, site, location, links)
            json_games.append(json_game)

        return json_games

    def get_game_entries(self, soup):
        """
        Return a list of elements containing games. Usually divs or rows.
        """
        schedule_table = soup.find('table', class_='list')
        headers = [header.text.upper().strip() for header in schedule_table.tr.find_all('th')]
        headers = self.get_clean_headers(headers)

        games = []
        for row in schedule_table.find_all('tr'):
            if row.th:
                # It contains headers
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
        opponent = game['OPPONENT'].text
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

        # @TODO: They don't have any posted :(

        return media_urls

    def get_game_time(self, game):
        """
        Return a datetime object of the games start time.
        """
        time_string = game['TIME'].text

        if "TBA" in time_string:
            time_string = "12:00 AM"
        return get_datetime_from_string(time_string)

    def get_game_date(self, game, years):
        """
        Return a datetime object of the games start date.
        """
        date_string = game['DATE'].text.upper().strip()
        if re.search(r'SEP|OCT|NOV|DEC', date_string):
            date_string = date_string + " %i" % years[0]
        else:
            date_string = date_string + " %i" % years[1]
        
        print date_string
        return get_datetime_from_string(date_string)

    def get_clean_headers(self, headers):
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

    def get_schedule_years(self, soup):
        """
        Return two integers representing the years of this schedule
        """
        page_title = soup.find('div', class_='listname').text
        year_string = re.sub(r'[^\d-]', '', page_title)
        years = year_string.split("-")
        n_years = []
        for year in years:
            if len(year) == 2:
                year = "20" + year
            if len(year) == 4:
                n_years.append(int(year))

        return n_years
