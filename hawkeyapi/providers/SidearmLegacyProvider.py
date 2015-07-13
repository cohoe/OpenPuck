#!/usr/bin/env python

from Provider import *


class SidearmLegacyProvider(Provider):
    def __init__(self, index_url):
        """
        Constructor
        """
        Provider.__init__(self)

        # Set up the URL information for this provider
        self.set_provider_urls(index_url)

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
        
        for linebreak in soup.find_all('br'):
            linebreak.replace_with(" ")

        json_games = []

        game_entries = self.get_game_entries(soup)
        headers = self.get_table_headers(soup)

        for entry in game_entries:
            cells = entry.find_all('td')

            # Game ID
            game_id = int(entry["id"].split("_")[-1])
            # Location
            location_col_index = get_list_index(headers, "LOCATION")
            raw_location = cells[location_col_index].text.strip()
            location = self.get_normalized_location(raw_location)
            # Opponent
            opponent_col_index = get_list_index(headers, "OPPONENT")
            raw_opponent = cells[opponent_col_index].text.strip()
            opponent = self.get_normalized_opponent(raw_opponent)
            # Site
            if cells[location_col_index].span:
                raw_site = cells[location_col_index].span['class'][0]
            else:
                raw_site = "away"

            site = self.get_normalized_site(raw_site)

            # Details
            details_soup = self.get_game_details(game_id)
            links = self.get_game_media_urls(details_soup)

            # Date and Time
            date_col_index = get_list_index(headers, "DATE")
            date_string = cells[date_col_index].text.strip()
            time_string = details_soup.td.find_all('em')[1].text.strip()

            # Sometimes they put a - in the dates to indicate multiple.
            # The bastards...
            if "-" in date_string:
                month, year, start, end = self.get_date_range(date_string)

                for day in range(start, end):
                    date_string = "%i/%i/%i" % (month, day, year)
                    timestamp = self.get_timestamp(date_string, time_string)
                    json_game = self.get_json_entry(game_id, timestamp,
                                                    opponent, site,
                                                    location, links)
                    json_games.append(json_game)
            else:
                timestamp = self.get_timestamp(date_string, time_string)
                json_game = self.get_json_entry(game_id, timestamp, opponent,
                                                site, location, links)
                json_games.append(json_game)

        return json_games

    def get_timestamp(self, date_string, time_string):
        """
        Make a timestamp for the given information.
        """
        time_string = time_string.upper().replace('.', '')

        # Schedules often give a TBA. Set this to midnight since no game
        # will actually start at midnight.
        if "TBA" in time_string or time_string == "":
            time_string = "12:00 AM"

        if "NOON" in time_string:
            time_string = "12:00 PM"

        if "/" in time_string:
            time_string = time_string.split("/")[0]
            if ":" in time_string:
                time_format = "%I:%M %p %Z"
            else:
                time_format = "%I %p %Z"
        elif ":" in time_string:
            time_format = "%I:%M %p"
        else:
            time_format = "%I %p"

        date_format = "%m/%d/%Y"

        return get_combined_timestamp(date_string, date_format,
                                      time_string, time_format)

    def get_normalized_site(self, raw_site):
        """
        Return a normalized word indiciating the site of the game.
        """
        if "home" in raw_site:
            return "home"
        elif "away" in raw_site:
            return "away"
        elif "neutral" in raw_site:
            return "neutral"
        else:
            return "UNKNOWN"

    def get_game_details(self, game_id):
        """
        Get the extras box for a given game
        """
        links_url = self.urls['schedule_detail'] + "?id=%i" % game_id
        html = get_html_from_url(links_url)
        soup = BeautifulSoup(html)

        return soup

    def get_game_media_urls(self, soup):
        """
        Locate the media URLs from the details box.
        """
        media_urls = {
            'video': False,
            'audio': False,
            'stats': False,
        }

        stats_string = soup.find(text="Live Stats")
        if stats_string:
            stats_url = stats_string.parent['href']
            media_urls['stats'] = stats_url

        return media_urls

    def get_game_entries(self, soup):
        schedule_table = soup.find_all('table', 'default_dgrd')[0]

        entries = []
        for child in schedule_table.children:
            child_soup = BeautifulSoup(unicode(child))
            cells = child_soup.find_all('td')
            if cells:
                entries.append(child)

        return entries

    def get_table_headers(self, soup):
        """
        Return an upper-case list of all of the column headers from the
        schedule table.
        """
        schedule_table = soup.find_all('table', 'default_dgrd')[0]

        header_elements = schedule_table.find_all('th')
        headers = []
        for header in header_elements:
            if header.text or header.text != "":
                n_header = header.text.upper().strip()
                n_header = re.sub(r'[^\w+]$', '', n_header)
                headers.append(n_header)

        return headers
