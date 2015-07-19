#!/usr/bin/env python

from Provider import *


class SidearmLegacyProvider(Provider):
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
            'schedule': "%s://%s/schedule.aspx?%s" % (url_obj.scheme, url_obj.netloc, url_obj.query),
            'schedule_detail': get_base_from_url(index_url) + "/services/schedule_detail.aspx",
        }

    def get_schedule(self):
        """
        Return a list of objects of the schedule.
        """
        soup = BeautifulSoup(self.get_schedule_from_web())

        # Years
        schedule_years = self.get_data_years(soup.title.text)

        games = []
        game_entries = self.get_game_entries(soup)

        for game in game_entries:
            # Game ID
            game_id = int(game["ID"].split("_")[-1])
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
            game_time = self.get_game_time(details_soup)
            game_date = self.get_game_date(game)
            timestamp = get_combined_timestamp(game_date, game_time)
            # Conference
            conference = self.get_game_conference(game)

            game = ScheduleEntry(game_id, timestamp, opponent, site, location, links, conference, schedule_years)
            games.append(game)

        return games

    def get_game_entries(self, soup):
        """
        Return a list of elements containing games. Usually divs or rows.
        """
        schedule_table = soup.find('table', 'default_dgrd')
        headers = []
        for header in schedule_table.tr.find_all('th'):
            raw_header = header.text.upper().strip()
            raw_header = re.sub(r'[^\w ]', '', raw_header)
            if raw_header == '' or raw_header == 'CHA' or raw_header == 'AHA':
                # Its the Clarkson conference header
                raw_header = 'CONF'
            headers.append(raw_header)

        games = []
        for row in schedule_table.find_all('tr', class_=['schedule_dgrd_item', 'schedule_dgrd_alt']):
            game = {}
            for i, cell in enumerate(row.find_all('td')):
                game[headers[i]] = cell

            game['CLASS'] = row['class']
            game['ID'] = row['id']
            games.append(game)

        return games

    def get_game_location(self, game):
        """
        Return a normalized string of the games location.
        """

        return self.get_normalized_location(game['LOCATION'].text)

    def get_game_site(self, game):
        """
        Return a normalized string of the games site classification.
        """
        location_element = game['LOCATION']

        if location_element.span:
            raw_site = location_element.span['class'][0]
        else:
            raw_site = "away"

        return self.get_normalized_site(raw_site)

    def get_game_opponent(self, game):
        """
        Return a normalized string of the games opponent.
        """

        return self.get_normalized_opponent(game['OPPONENT'].text)

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
        media_urls = {}

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

        return get_datetime_from_string(time_string)

    def get_game_date(self, game):
        """
        Return a datetime object of the games start date.
        """

        return get_datetime_from_string(game['DATE'].text.strip())

    def get_game_conference(self, game):
        """
        Is this a conference game?
        """
        return bool(game['CONF'].img)
