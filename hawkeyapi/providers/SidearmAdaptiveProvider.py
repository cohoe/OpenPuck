#!/usr/bin/env python

from Provider import *


class SidearmAdaptiveProvider(Provider):
    def __init__(self, team):
        """
        Constructor
        """
        Provider.__init__(self, team)

        # Set up the URL information for this provider
        index_url = team.website

        self.set_provider_urls(index_url)
        self.provider_name = __name__

    def set_provider_urls(self, index_url):
        """
        Set our URLs so we can reference them later.
        """
        url_obj = urlparse(index_url)
        url_queries = url_obj.query.split('&')
        for query in url_queries:
            if "path" in query:
                self.sport = query.split('=')[1]

        self.urls = {
            'index': index_url,
            'schedule': "%s://%s/schedule.aspx?%s" % (url_obj.scheme, url_obj.netloc, url_obj.query),
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
            # Game ID
            game_id = game['id'].split('_')[-1]
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
            conference = self.get_game_conference(game)

            game = ScheduleEntry(game_id, game_date, game_time, opponent, site,
                                 location, links, conference,
                                 season.league, season.id, self.team_id)
            games.append(game)

        return games

    def get_game_entries(self, soup):
        """
        Return a list of elements containing games. Usually divs or rows.
        """
        return soup.find_all('div', class_='schedule_game')

    def get_game_location(self, game):
        """
        Return a normalized string of the games location.
        """
        facility_element = game.find('div', class_='schedule_game_facility')
        location_element = game.find('div', class_='schedule_game_location')
        facility = ""
        if facility_element:
            facility = self.get_normalized_location(facility_element.text)
        location = self.get_normalized_location(location_element.text)
        location = ' '.join([facility, location])
        location = location.lstrip()
        return location

    def get_game_site(self, game):
        """
        Return a normalized string of the games site
        classification (home, away, neutral)
        """
        parent_class = game['class'][1:2][0]
        if parent_class == "" or not parent_class:
            parent_class = "home"

        return self.get_normalized_site(parent_class)

    def get_game_opponent(self, game):
        """
        Return a normalized string of the games opponent.
        """
        site = self.get_game_site(game)

        opp_element = game.find('div', class_='schedule_game_opponent_name')
        opponent = opp_element.text

        return self.get_normalized_opponent(opponent)

    def get_game_media_urls(self, game):
        """
        Return a normalized dictionary of media URLs.
        """
        media_urls = {}

        m_element = game.find('div', class_='schedule_game_multimedia_links')
        if not m_element:
            return media_urls

        a_elements = m_element.find_all('a', class_='schedule_game_media_link')
        for link in a_elements:
            link_text = link.text.upper()
            if "STATS" in link_text:
                media_urls['stats'] = link['href']
            if "AUDIO" in link_text:
                media_urls['audio'] = link['href']
            if "VIDEO" in link_text:
                media_urls['video'] = link['href']

        return media_urls

    def get_game_date(self, game, years):
        """
        Return a date object of the games start time. Note that it will
        have no time so it needs to be paired with a game_time object.
        """
        date_element = game.find('div', class_='schedule_game_opponent_date')
        date_string = date_element.text.upper().strip()

        return get_date_from_string(date_string, years)

    def get_game_time(self, game):
        """
        Return a time object of the games start time. Note that it will
        have todays date so it needs to be combined with a game_date
        object.
        """
        t_element = game.find('div', class_='schedule_game_opponent_time')
        time_string = t_element.text.strip()
        return get_time_from_string(time_string)

    def get_game_conference(self, game):
        """
        Return if this is a conference game or not
        """
        element = game.find('div', class_='schedule_games_conference')
        return bool(element)

    def get_schedule_url_for_season(self, season):
        """
        Return the full URL of the schedule for a given season.
        """
        soup = BeautifulSoup(self.get_schedule_from_web())
        sched_select = soup.find(id='ctl00_cplhMainContent_ddlPastschedules2')

        # 20150911 They made some of the dropdowns have full years. Ugh.
        # AND THEY MIX THEM IN THE SAME SCHOOL!!!
        test_option = sched_select.find('option')
        for option in sched_select.find_all('option'):
            text = option.text.strip()
            if len(text) == 9:
                # Long
                season_id = "%s-%s" % (season.start_year, season.end_year)
            elif len(text) == 7:
                # Short
                season_id = season.short_id

            if text == season_id:
                schedule_number = option['value']

        return "%s/schedule.aspx?path=%s&schedule=%s" % (self.server, self.sport, schedule_number)
