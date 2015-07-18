#!/usr/bin/env python

from Provider import *


class NeulionLegacyProvider(Provider):
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
        soup = BeautifulSoup(get_html_from_url(index_url))

        self.urls = {
            'index': index_url,
            'schedule': self.server + soup.find(id='section-menu').find('a', text="Schedules/Results")['href']
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
            game_date = self.get_game_date(game, schedule_years)
            game_time = self.get_game_time(game)
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
        schedule_table = soup.find('table', class_="ScheduleTable")
        headers = [header.text.upper().strip() for header in schedule_table.find_all('th')]
        results = []
        for row in schedule_table.find_all('tr'):
            game = {}
            for i, cell in enumerate(row.find_all('td')):
                game[headers[i]] = cell
            if game and len(game.keys()) == len(headers):
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
        if "highlight" in game['OPPONENT'].font['class']:
            return self.get_normalized_site("home")
        elif "sm" in game['OPPONENT'].font['class']:
            return self.get_normalized_site("away")
        else:
            return self.get_noramlized_site("unknown")

    def get_game_opponent(self, game):
        """
        Return a normalized string of the games opponent.
        """
        return self.get_normalized_opponent(game['OPPONENT'].text)

    def get_game_media_urls(self, game):
        """
        Locate the media URLs from the details box.
        """
        media_urls = {
            'audio': False,
            'video': False,
            'stats': False,
        }

        media_element = game['MEDIA']
        for link in media_element.find_all('a'):
            link_text = link.text.strip()
            # @TODO This is somewhat institution specific. Likely
            # need to add more stuff here.
            if "ILDN" in link_text:
                media_urls['video'] = link['href']

            title = link.get("title")
            if title and "Live Stats" in title:
                media_urls['stats'] = self.server + link['href']

            if "iheart" in link['href']:
                media_urls['audio'] = link['href']

        return media_urls

    def get_game_time(self, game):
        """
        Return a datetime object of the games start time.
        """
        time_header = ""
        for header in game.keys():
            if "TIME" in header:
                time_header = header
                break

        time_string = game[time_header].text.strip()
        if "TBA" in time_string:
            time_string = "12:00 AM"

        return get_datetime_from_string(time_string)

    def get_game_date(self, game, years):
        """
        Return a datetime object of the games start date.
        """
        date_string = game['DATE'].text.strip().upper()
        if "-" in date_string:
            date_string = date_string.split("-")[0].strip()

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
        # You people should be ashamed of yourselves....
        page_title = soup.table.table.td.text
        year_string = re.sub(r'[^\d-]', '', page_title)
        years = year_string.split("-")
        n_years = []
        for year in years:
            if len(year) == 2:
                year = "20" + year
            if len(year) == 4:
                n_years.append(int(year))

        return n_years