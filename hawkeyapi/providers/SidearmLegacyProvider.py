#!/usr/bin/env python

from Provider import *


class SidearmLegacyProvider(Provider):
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

        self.urls = {
            'index': index_url,
            'schedule': "%s://%s/schedule.aspx?%s" % (url_obj.scheme, url_obj.netloc, url_obj.query),
            'schedule_detail': get_base_from_url(index_url) + "/services/schedule_detail.aspx",
        }

    def get_schedule(self):
        """
        Return a list of JSON objects of the schedule.
        """
        html = self.get_schedule_from_web()
        soup = BeautifulSoup(html)

        json_games = []

        game_entries = self.get_game_entries(soup)
        self.schedule_headers = self.get_table_headers(soup)

        for game in game_entries:
            # Game ID
            game_id = int(game["id"].split("_")[-1])
            # Location
            location = self.get_game_location(game)
            # Site
            site = self.get_game_site(game)
            # Opponent
            opponent = self.get_game_opponent(game)
            # Links
            details_soup = self.get_game_details(game_id)
            links = self.get_game_media_urls(details_soup)
            # Timestamp
            timestamp = self.get_game_timestamp(game, details_soup)

            json_game = self.get_json_entry(game_id, timestamp, opponent, site, location, links)
            json_games.append(json_game)

        return json_games

    def get_game_entries(self, soup):
        """
        Return a list of elements containing games. Usually divs or rows.
        """
        return soup.find_all('tr', class_=['schedule_dgrd_alt', 'schedule_dgrd_item'])

    def get_table_headers(self, soup):
        """
        Return an upper-case list of all of the column headers from the
        schedule table.
        """
        schedule_table = soup.find('table', 'default_dgrd')

        header_elements = schedule_table.find_all('th')
        headers = []
        for header in header_elements:
            if header.text or header.text != "":
                n_header = header.text.upper().strip()
                n_header = re.sub(r'[^\w+]$', '', n_header)
                headers.append(n_header)

        return headers

    def get_game_location(self, game):
        """
        Return a normalized string of the games location.
        """
        location_col_index = get_list_index(self.schedule_headers, "LOCATION")
        raw_location = game.find_all('td')[location_col_index].text
        
        return self.get_normalized_location(raw_location)

    def get_game_site(self, game):
        """
        Return a normalized string of the games site classification.
        """
        location_col_index = get_list_index(self.schedule_headers, "LOCATION")
        location_element = game.find_all('td')[location_col_index]

        if location_element.span:
            raw_site = location_element.span['class'][0]
        else:
            raw_site = "away"

        return self.get_normalized_site(raw_site)

    def get_game_opponent(self, game):
        """
        Return a normalized string of the games opponent.
        """
        opponent_col_index = get_list_index(self.schedule_headers, "OPPONENT")
        raw_opponent = game.find_all('td')[opponent_col_index].text

        return self.get_normalized_opponent(raw_opponent)

    def get_game_details(self, game_id):
        """
        Get the extras box for a given game
        """
        links_url = self.urls['schedule_detail'] + "?id=%i" % game_id
        html = get_html_from_url(links_url)
        soup = BeautifulSoup(html)

        return soup

    def get_game_media_urls(self, details):
        """
        Locate the media URLs from the details box.
        """
        media_urls = {
            'video': False,
            'audio': False,
            'stats': False,
        }

        stats_string = details.find(text="Live Stats")
        if stats_string:
            stats_url = stats_string.parent['href']
            media_urls['stats'] = stats_url

        return media_urls

    def get_game_time(self, details):
        """
        Return a datetime object of the games start time.
        """
        time_string = details.td.find_all('em')[1].text.strip()
        time_string = time_string.upper().replace('.', '')

        if "TBA" in time_string or time_string == "":
            time_string = "12:00 AM"
        if "NOON" in time_string:
            time_string = "12:00 PM"

        return get_datetime_from_string(time_string)

    def get_game_date(self, game):
        """
        Return a datetime object of the games start date.
        """
        date_col_index = get_list_index(self.schedule_headers, "DATE")
        date_string = game.find_all('td')[date_col_index].text.strip()
        if "-" in date_string:
            date_string = date_string.split("-")[0].strip()

        return get_datetime_from_string(date_string)

    def get_game_timestamp(self, game, details):
        """
        Return a datetime object representing the start time of the game.
        """
        game_time = self.get_game_time(details)
        game_date = self.get_game_date(game)

        return datetime.combine(game_date, game_time.time())
