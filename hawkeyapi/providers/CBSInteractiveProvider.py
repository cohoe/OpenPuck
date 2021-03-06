#!/usr/bin/env python

from Provider import *


class CBSInteractiveProvider(Provider):
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

        # Really? Really? Ugh...
        index_file = url_obj.path.split("/")[-1]
        schedule_path = "/".join(url_obj.path.split("/")[:-1]) + "/sched"
        schedule_file = index_file.replace("-main", "")
        self.schedule_file = schedule_file.replace("body", "sched")
        self.sport = url_obj.path.split("/")[2]

        self.urls = {
            'index': index_url,
            'schedule': "%s://%s%s/%s" % (url_obj.scheme, url_obj.netloc,
                                          schedule_path, self.schedule_file),
            'event_data': "%s://%s/data/xml/events/%s/" % (url_obj.scheme,
                                                           url_obj.netloc,
                                                           self.sport),
        }

    def get_schedule(self):
        """
        Return a list of JSON objects of the schedule.
        """
        url = self.get_schedule_url_for_season(self.season)
        soup = get_soup_from_content(get_html_from_url(url))

        game_entries = self.get_game_entries(soup)
        games = []

        for game in game_entries:
            # Game ID
            r_game_id = game['id']
            game_id = self.get_id_from_string(game['id'])
            # Details
            details_soup = self.get_game_details(self.season.start_year,
                                                 r_game_id)
            # Determine head-to-head
            raw_h2h = details_soup.find('headtohead')['flag']
            if raw_h2h == 'no':
                # Skip this game since its not ours
                continue
            # Test for postponed games
            try:
                postponed = details_soup.find('outcome_score')['data']
                if postponed.upper().strip() == "POSTPONED":
                    # Skip it
                    continue
            except KeyError:
                pass
            # Location
            location = self.get_game_location(details_soup)
            # Site
            site = self.get_game_site(details_soup)
            # Opponent
            opponent = self.get_game_opponent(details_soup)
            # Links
            links = self.get_game_media_urls(details_soup)
            # Timestamp
            game_date = self.get_game_date(details_soup, self.season.years())
            game_time = self.get_game_time(details_soup)
            # Conference
            conference = self.get_game_conference(game)

            game = ScheduleEntry(game_id, game_date, game_time, opponent,
                                 site, location, links, conference,
                                 self.season.league, self.season.id,
                                 self.team_id, self.is_women)
            games.append(game)

        return games

    @classmethod
    def get_game_entries(cls, soup):
        """
        Return a list of elements containing games. Usually divs or rows.
        """
        game_entries = []

        for row in soup.find_all('tr', class_='event-listing'):
            game_entries.append(row)

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

        # If it has no home_element, then its likely an exhibition
        home_element = game.find('home')
        if home_element:
            home_code = game.find('home')['code']
        else:
            return self.get_normalized_site("home")

        if my_code == home_code:
            return self.get_normalized_site("home")

        return self.get_normalized_site("away")

    def get_game_opponent(self, game):
        """
        Return a normalized string of the games opponent.
        """
        my_code = game.find('event')['school']

        home_element = game.find('home')
        if home_element:
            home_code = game.find('home')['code']
            if my_code == home_code:
                # I am home, get the away team
                raw_opponent = game.find('away')['opp']
            else:
                # Sometimes they dont explicitly state the opponent
                if home_element.has_attr("opp"):
                    raw_opponent = home_element['opp']
                else:
                    raw_opponent = home_element['code']
        else:
            # Its one of those funky exhibitions
            raw_opponent = game.find('event')['event_name']

        return self.get_normalized_opponent(raw_opponent)

    @classmethod
    def get_game_media_urls(cls, game):
        """
        Locate the media URLs from the details box.
        """
        media_urls = {}

        media_elements = game.find_all('media')
        for element in media_elements:
            if element['title'] == "Gametracker":
                media_urls['stats'] = element['url']

        return media_urls

    @classmethod
    def get_game_time(cls, game):
        """
        Return a time object of the games start time.
        """
        time_string = game.find('detail')['time'].strip()

        return get_time_from_string(time_string)

    @classmethod
    def get_game_date(cls, game, years):
        """
        Return a date object of the games start date.
        """
        date_string = game.find('detail')['date'].strip()
        date_string = date_string.upper().replace('.', '')
        if "SEPT" in date_string:
            date_string = re.sub(r'SEPT', 'SEP', date_string)

        return get_date_from_string(date_string, years)

    def get_game_details(self, year, game_id):
        """
        Return the detail schedule information for a game.
        """
        game_url = self.urls['event_data'] + "%i/%s.xml" % (year, game_id)
        return get_soup_from_content(get_html_from_url(game_url))

    @classmethod
    def get_game_conference(cls, game):
        """
        Is this a conference game? Some teams dont tell us
        so this has to be None... :(
        """
        raw_opponent = game.find_all('td')[1].text
        if "*" in raw_opponent:
            return True
        return None

    def get_schedule_url_for_season(self, season):
        """
        Return the full URL of the schedule for a given season.
        """
        # Try the archive
        file_ = re.sub(r'\.html', "-%i.html" % season.start_year,
                       self.schedule_file)
        directory = "archive"
        url = "%s/sports/%s/%s/%s" % (self.server, self.sport, directory, file_)

        r = requests.get(url)
        if r.status_code == 404:
            # Then its probably active
            directory = "sched"
            url = "%s/sports/%s/%s/%s" % (self.server, self.sport, directory,
                                          self.schedule_file)

        return url

    @classmethod
    def detect(cls, soup):
        """
        Determine of the URL is handled by this provider.
        :param soup: The site content object to check.
        :return: Boolean of whether this site is mine.
        """
        if soup.body.get('class') is not None:
            if 'bsi-full' in soup.body.get('class'):
                return True

        return False
