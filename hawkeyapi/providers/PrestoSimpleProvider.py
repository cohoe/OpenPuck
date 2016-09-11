#!/usr/bin/env python

from Provider import *


class PrestoSimpleProvider(Provider):
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
        url_obj = urlparse(index_url)

        self.sport = url_obj.path.split("/")[2]
        season = self.season.short_id
        schedule_url = "%s://%s/sports/%s/%s/schedule" % (url_obj.scheme, url_obj.netloc, self.sport, season)

        self.urls = {
            'index': index_url,
            'schedule': schedule_url,
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
            game_date = self.get_game_date(game, self.season.years())
            game_time = self.get_game_time(game)
            # Conference
            conference = self.get_game_conference(game)
            # Game ID
            game_id = self.get_gameid_from_date_time(game_date, game_time)

            game = ScheduleEntry(game_id, game_date, game_time, opponent, site,
                                 location, links, conference,
                                 self.season.league, self.season.id,
                                 self.team_id, self.is_women)
            games.append(game)

        return games

    def get_game_entries(self, soup):
        """
        Return a list of elements containing games.
        """
        games = []
        index = 0
        game = []

        table_element = soup.find('table', class_='schedule')
        for row in table_element.find_all('tr', class_=['schedule-row0', 'schedule-row1']):
            if "schedule-row%i" % index in row['class']:
                # This row is for the current game
                game.append(row)
            else:
                # This row is for a different game
                games.append(game)
                # Reset the index and game holder
                game = []
                if index == 0:
                    index = 1
                else:
                    index = 0
                # Append to a new game
                game.append(row)

        # Flush the last bits of game we have
        games.append(game)
        return games

    def get_game_site(self, game):
        """
        Return a normalized string of the games site classification.
        """
        opponent_element = game[0].find_all('td')[1]
        if opponent_element.b:
            return self.get_normalized_site("home")
        else:
            return self.get_normalized_site("away")

    def get_game_opponent(self, game):
        """
        Return a normalized string of the games opponent.
        """
        raw_opponent = game[0].find_all('td')[1].text.strip()
        raw_opponent = re.sub(r'^at ', '', raw_opponent)
        return self.get_normalized_opponent(raw_opponent)

    def get_game_media_urls(self, game):
        """
        Locate the media URLs from the details box.
        """
        media_urls = {}

        if len(game) >= 2:
            # It's a Maine-style dual-row
            second_row_elements = game[1].find_all('td')
            if len(second_row_elements) == 1:
                links_element = second_row_elements[0]
            else:
                # They put a "Links:" header elemenet in there
                links_element = second_row_elements[1]
        else:
            # It's a UNH-style single-row
            links_element = game[0].find_all('td')[5]

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
        Return a time object of the games start time.
        """
        # Games can be multiple rows. Figure out where the field is based
        # on what we've see from various instances.
        # @TODO: This needs to be fully tested
        col_index = 3
        if len(game) >= 2:
            col_index = 4
        time_string = game[0].find_all('td')[col_index].text.strip().upper()
        if re.search(r'[a-zA-Z]{3,}', time_string):
            time_string = "12:00 AM"

        return get_time_from_string(time_string)

    def get_game_date(self, game, years):
        """
        Return a date object of the games start date.
        """
        # The field only gives us the day of the month
        date_string = game[0].find_all('td')[0].text.upper().strip()

        return get_date_from_string(date_string, years)

    def get_game_conference(self, game):
        """
        Is this a conference game?
        """
        raw_opponent = game[0].find_all('td')[1].text.strip()
        return ("*" in raw_opponent)

    def get_schedule_url_for_season(self, season):
        """
        Return the full URL of the schedule for a given season.
        """
        return "%s/sports/%s/%s/schedule" % (self.server, self.sport, season.short_id)

    @classmethod
    def detect(cls, soup):
        """
        Determine of the URL is handled by this provider.
        :param soup: The site content object to check.
        :return: Boolean of whether this site is mine.
        """
        if soup.find(id='page-background') is not None:
            return True

        return False
