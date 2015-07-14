#!/usr/bin/env python

from Provider import *


class CBSInteractiveProvider(Provider):
    def __init__(self, index_url):
        """
        Constructor
        """
        Provider.__init__(self)

        self.set_provider_urls(index_url)
        self.provider_name = __name__

    def set_provider_urls(self, index_url):
        """
        Set our URLs so we can reference them later.
        """
        url_obj = urlparse(index_url)
        
        # Really? Really? Ugh...
        index_file = url_obj.path.split("/")[-1]
        schedule_path = "/".join(url_obj.path.split("/")[:-1]) + "/sched"
        schedule_file = index_file.replace("-main", "")
        schedule_file = schedule_file.replace("body", "sched")
        sport = url_obj.path.split("/")[2]

        self.urls = {
            'index': index_url,
            'schedule': "%s://%s%s/%s" % (url_obj.scheme, url_obj.netloc, schedule_path, schedule_file),
            'event_data': "%s://%s/data/xml/events/%s/" % (url_obj.scheme, url_obj.netloc, sport),
        }

    def get_schedule(self):
        """
        Return a list of JSON objects of the schedule.
        """
        soup = BeautifulSoup(self.get_schedule_from_web())

        json_games = []

        year = self.get_schedule_year(soup)
        game_entries = self.get_game_entries(soup)

        for game in game_entries:
            # Game ID
            game_id = int(game['id'])
            # Details
            details_soup = self.get_game_details(year, game_id)
            # Location
            location = self.get_game_location(details_soup)
            # Site
            site = self.get_game_site(details_soup)
            # Opponent
            opponent = self.get_game_opponent(details_soup)
            # Links
            links = self.get_game_media_urls(details_soup)
            # Timestamp
            timestamp = self.get_game_timestamp(details_soup)

            json_game = self.get_json_entry(game_id, timestamp, opponent, site, location, links)
            json_games.append(json_game)

        return json_games

    def get_game_entries(self, soup):
        """
        Return a list of elements containing games. Usually divs or rows.
        """
        game_entries = []

        for row in soup.find(id='schedtable').find_all('tr'):
            cells = row.find_all('td')
            try:
                if cells[0]['class'][0] == "row-text":
                    game_entries.append(row)
            except KeyError:
                continue

        return game_entries


    def get_game_location(self, game):
        """
        Return a normalized string of the games location.
        """
        raw_location = game.find('detail')['location']
        
        return self.get_normalized_location(raw_location)

    def get_game_site(self, game):
        """
        Return a normalized string of the games site classification.
        """
        my_code = game.find('event')['school']

        is_neutral = game.find('event')['neutral_site']
        if is_neutral == "yes":
            return self.get_normalized_site("neutral")

        home_code = game.find('home')['code']
        if my_code == home_code:
            return self.get_normalized_site("home")

        return self.get_normalized_site("away")

    def get_game_opponent(self, game):
        """
        Return a normalized string of the games opponent.
        """
        my_code = game.find('event')['school']
        home_code = game.find('home')['code']

        if my_code == home_code:
            # I am home, get the away team
            raw_opponent = game.find('away')['opp']
        else:
            raw_opponent = game.find('home')['opp']
            
        return self.get_normalized_opponent(raw_opponent)

    def get_game_media_urls(self, game):
        """
        Locate the media URLs from the details box.
        """
        media_urls = {
            'video': False,
            'audio': False,
            'stats': False,
        }

        media_elements = game.find_all('media')
        for element in media_elements:
            if element['title'] == "Gametracker":
                media_urls['stats'] = element['url']

        return media_urls

    def get_game_time(self, game):
        """
        Return a datetime object of the games start time.
        """
        time_string = game.find('detail')['time'].strip()

        if "TBA" in time_string or time_string == "":
            time_string = "12:00 AM"

        return get_datetime_from_string(time_string)

    def get_game_date(self, game):
        """
        Return a datetime object of the games start date.
        """
        date_string = game.find('detail')['date'].strip()
        date_string = date_string.upper().replace('.', '')
        if "SEPT" in date_string:
            date_string = re.sub(r'SEPT', 'SEP', date_string)

        return get_datetime_from_string(date_string)

    def get_game_timestamp(self, game):
        """
        Return a datetime object representing the start time of the game.
        """
        game_date = self.get_game_date(game)
        game_time = self.get_game_time(game)

        return datetime.combine(game_date, game_time.time())

    def get_schedule_year(self, soup):
        """
        Figure out what year we are in.
        """
        title = soup.find('div', class_='compositetitle').text
        return int(title.split("-")[0])

    def get_game_details(self, year, game_id):
        """
        Return the detail schedule information for a game.
        """
        game_url = self.urls['event_data'] + "%i/%i.xml" % (year, game_id)
        return BeautifulSoup(get_html_from_url(game_url))
