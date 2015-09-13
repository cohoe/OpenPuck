#!/usr/bin/env python

from Provider import *


class PrestoLegacyProvider(Provider):
    def __init__(self, team):
        """
        Constructor
        """
        Provider.__init__(self, team)

        index_url = team.website
        self.set_provider_urls(index_url)
        self.provider_name = __name__

    def set_provider_urls(self, index_url):
        """
        Set our URLs so we can reference them later.
        """
        url_obj = urlparse(index_url)

        self.sport = url_obj.path.split("/")[2]
        season = DATE_SEASON
        schedule_url = "%s://%s/sports/%s/%s/schedule" % (url_obj.scheme, url_obj.netloc, self.sport, season)

        self.urls = {
            'index': index_url,
            'schedule': schedule_url,
        }

    def get_schedule(self, season):
        """
        Return a list of JSON objects of the schedule.
        """
        url = self.get_schedule_url_for_season(season)
        soup = BeautifulSoup(get_html_from_url(url))

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
            game_date = self.get_game_date(game, season.years())
            game_time = self.get_game_time(game)
            timestamp = get_combined_timestamp(game_date, game_time)
            # Game ID
            game_id = self.get_gameid_from_timestamp(timestamp)
            # Conference
            conference = self.get_game_conference(game)

            # They don't have game_id's, so lets build one
            game = ScheduleEntry(game_id, game_date, game_time, opponent, site,
                                 location, links, conference, season.league, season.id)
            games.append(game)

        return games

    def get_game_entries(self, soup):
        """
        Return a list of elements containing games.
        """
        schedule_table = soup.find('table', class_='schedule')
        # The bastards dont use th's!!!!
        headers = [header.text.upper().strip() for header in schedule_table.tr.find_all('td')]

        games = []
        for row in schedule_table.find_all('tr', class_=["schedule-home", "schedule-away"]):
            if len(row.find_all('td')) < len(headers):
                # It's a second row that we don't care about
                continue

            game = {}
            for i, cell in enumerate(row.find_all('td')):
                game[headers[i]] = cell

            game['CLASS'] = row['class']
            games.append(game)

        return games

    def get_game_site(self, game):
        """
        Return a normalized string of the games site classification.
        """
        if "schedule-home" in game['CLASS']:
            return self.get_normalized_site("home")
        elif "schedule-away" in game['CLASS']:
            return self.get_normalized_site("away")
        else:
            return self.get_noramlized_site("unknown")

    def get_game_opponent(self, game):
        """
        Return a normalized string of the games opponent.
        """
        raw_opponent = game['OPPONENT'].text.strip()
        raw_opponent = re.sub(r'^at ', '', raw_opponent)
        return self.get_normalized_opponent(raw_opponent)

    def get_game_media_urls(self, game):
        """
        Locate the media URLs from the details box.
        """
        media_urls = {}

        links_element = game['LINKS']

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
        time_string = game['STATUS'].text.strip().upper()
        if re.search(r'[a-zA-Z]{3,}', time_string):
            time_string = "12:00 AM"

        return get_time_from_string(time_string)

    def get_game_date(self, game, years):
        """
        Return a date object of the games start date.
        """
        # The field only gives us the day of the month
        date_string = game['DATE'].text.upper().strip()

        return get_date_from_string(date_string, years)

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
        return "%s/sports/%s/%s/schedule" % (self.server, self.sport, season.id)
