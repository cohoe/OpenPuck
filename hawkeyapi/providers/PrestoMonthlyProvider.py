#!/usr/bin/env python

from Provider import *


class PrestoMonthlyProvider(Provider):
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

        # Years
        page_title = soup.title.text
        schedule_years = self.get_data_years(page_title)
        month = ""

        json_games = []
        game_entries = self.get_game_entries(soup)
        for game in game_entries:
            if game['class'][0] == "month-title":
                if re.search(r'[a-zA-Z]{3}', game.text):
                    month = game.text
                continue
            if game['class'][0] == "month-sep":
                continue

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
            game_date = self.get_game_date(game, month, schedule_years)
            game_time = self.get_game_time(game)
            timestamp = datetime.combine(game_date, game_time.time())
            # Game ID
            game_id = get_id_from_timestamp(timestamp)

            json_game = self.get_json_entry(game_id, timestamp, opponent, site, location, links)
            json_games.append(json_game)

        return json_games

    def get_game_entries(self, soup):
        """
        Return a list of elements containing games. Usually divs or rows.
        In this case, we need it for months as well.
        """
        # Skip the first since its always an empty
        return soup.find('div', class_=['schedule-data', 'schedule-content']).find_all('tr')[1:]

    def get_game_site(self, game):
        """
        Return a normalized string of the games site classification.
        """
        # Neutral is given as a seperate element
        neutral_element = game.find('span', class_='e_neutralsite')
        if neutral_element:
            return self.get_normalized_site("neutral")

        # Others are given as a CSS class. Anything not explicit is assumed to be away.
        opponent_element = game.find('span', class_='e_opponent_name')
        if "e_home" in opponent_element['class']:
            return self.get_normalized_site("home")
        else:
            return self.get_normalized_site("away")

    def get_game_opponent(self, game):
        """
        Return a normalized string of the games opponent.
        """
        raw_opponent = game.find('span', class_='e_opponent_name').text
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
        links = game.find('td', class_='e_links').find_all('a')
        for link in links:
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
        time_string = game.find('td', class_='e_status').text.strip()

        return get_datetime_from_string(time_string)

    def get_game_date(self, game, month, years):
        """
        Return a datetime object of the games start date.
        """
        # The field only gives us the day of the month
        raw_date = game.find('td', class_='e_date').text.strip()
        day = int(re.sub('[^\d]+', '', raw_date))
        # Hence the need for an explicit month
        date_string = "%s %i" % (month, day)
        date_string = date_string.upper()

        return get_datetime_from_string(date_string, years)
