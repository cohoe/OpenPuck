#!/usr/bin/env python

from Provider import *


class NeulionLegacyProvider(Provider):
    def __init__(self, team):
        """
        Constructor
        """
        Provider.__init__(self, team)

        index_url = team.website['index_url']
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

            game = ScheduleEntry(game_id, timestamp, opponent, site, location, links, conference, season)
            games.append(game)

        return games

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
        media_urls = {}

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
        time_header = None
        for header in game.keys():
            if "TIME" in header:
                time_header = header
                break

        if time_header is None:
            time_string = "12:00 AM"
        else:
            time_string = game[time_header].text.strip()

        return get_datetime_from_string(time_string)

    def get_game_date(self, game, years):
        """
        Return a datetime object of the games start date.
        """
        date_string = game['DATE'].text.strip().upper()

        return get_datetime_from_string(date_string, years)

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
