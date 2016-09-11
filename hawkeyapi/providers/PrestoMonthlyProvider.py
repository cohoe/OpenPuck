#!/usr/bin/env python

from Provider import *


class PrestoMonthlyProvider(Provider):
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

        month = ""

        games = []
        game_entries = self.get_game_entries(soup)
        for game in game_entries:
            if game['class'][0] == "month-title":
                if re.search(r'[a-zA-Z]{3}', game.text):
                    month = game.text
                continue
            # @TODO: Why is this here?
            if game['class'][0] == "month-sep":
                continue

            # See if there is actually a game here.
            if not game.find('td', class_='e_date'):
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
            game_date = self.get_game_date(game, month, self.season.years())
            game_time = self.get_game_time(game)
            # Game ID
            game_id = self.get_gameid_from_date_time(game_date, game_time)
            # Conference
            conference = self.get_game_conference(game)

            game = ScheduleEntry(game_id, game_date, game_time, opponent, site,
                                 location, links, conference,
                                 self.season.league, self.season.id, self.team_id,
                                 self.is_women)
            games.append(game)

        return games

    def get_game_entries(self, soup):
        """
        Return a list of elements containing games. Usually divs or rows.
        In this case, we need it for months as well.
        """
        # Skip the first since its always an empty
        s_element = soup.find('div', class_=['schedule-data', 'schedule-content'])
        return s_element.find_all('tr')[1:]

    def get_game_site(self, game):
        """
        Return a normalized string of the games site classification.
        """
        # Neutral is given as a seperate element
        neutral_element = game.find('span', class_='e_neutralsite')
        if neutral_element:
            return self.get_normalized_site("neutral")

        # Others are given as a CSS class. Anything not
        # explicit is assumed to be away.
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
        media_urls = {}

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
        Return a time object of the games start time.
        """
        time_string = game.find('td', class_='e_status').text.strip()

        return get_time_from_string(time_string)

    def get_game_date(self, game, month, years):
        """
        Return a date object of the games start date.
        """
        # The field only gives us the day of the month
        raw_date = game.find('td', class_='e_date').text.strip()
        day = int(re.sub('[^\d]+', '', raw_date))
        # Hence the need for an explicit month
        date_string = "%s %i" % (month, day)
        date_string = date_string.upper()

        return get_date_from_string(date_string, years)

    def get_game_conference(self, game):
        """
        Return if this a conference game.
        """
        raw_opponent = game.find('td', class_='e_opponent').text
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
        if soup.find('a', href=True, text='PrestoSports'):
            if soup.find(id='fb-root') is not None:
                return True

        return False
