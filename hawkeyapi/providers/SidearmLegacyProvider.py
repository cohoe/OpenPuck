#!/usr/bin/env python

from Provider import *


class SidearmLegacyProvider(Provider):
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
        url_queries = url_obj.query.split('&')
        for query in url_queries:
            if "path" in query:
                self.sport = query.split('=')[1]

        detail_url = "/services/schedule_detail.aspx"
        self.urls = {
            'index': index_url,
            'schedule': "%s://%s/schedule.aspx?%s" % (url_obj.scheme, url_obj.netloc, url_obj.query),
            'schedule_detail': get_base_from_url(index_url) + detail_url,
        }

    def get_schedule(self, season):
        """
        Return a list of objects of the schedule.
        """
        url = self.get_schedule_url_for_season(season)
        soup = get_soup_from_content(get_html_from_url(url))

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
            game_date = self.get_game_date(game, season.years())
            # Conference
            conference = self.get_game_conference(game)

            game = ScheduleEntry(game_id, game_date, game_time, opponent, site,
                                 location, links, conference,
                                 season.league, season.id, self.team_id,
                                 self.is_women)
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
            if raw_header == '' or raw_header == 'CHA' or raw_header == 'AHA' or raw_header == 'CONFERENCE GAME':
                # Its the Clarkson-esqe conference header
                raw_header = 'CONF'
            headers.append(raw_header)

        games = []
        for row in schedule_table.find_all('tr', class_=['schedule_dgrd_item', 'schedule_dgrd_alt']):
            game = {}
            for i, cell in enumerate(row.find_all('td')):
                game[headers[i]] = cell

            game['CLASS'] = row['class']
            game['ID'] = row['id']
            # Sometimes they don't put the time in for conf/natty games.
            if game['TIMERESULT'].text.strip() != "":
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
        soup = get_soup_from_content(html)

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
        Return a time object of the games start time.
        """
        time_string = details.td.find_all('em')[1].text.strip()
        if "/" in time_string:
            time_string = time_string.split("/")[0]

        return get_time_from_string(time_string)

    def get_game_date(self, game, years):
        """
        Return a date object of the games start date.
        """

        return get_date_from_string(game['DATE'].text.strip(), years)

    def get_game_conference(self, game):
        """
        Is this a conference game?
        """
        return bool(game['CONF'].img)

    def get_schedule_url_for_season(self, season):
        """
        Return the full URL of the schedule for a given season.
        """
        soup = get_soup_from_content(self.get_schedule_from_web())
        sched_select = soup.find(id='ctl00_cplhMainContent_ddlPastschedules')
        for option in sched_select.find_all('option'):
            if option.text.strip() == season.short_id:
                schedule_number = option['value']

        return "%s/schedule.aspx?path=%s&schedule=%s" % (self.server, self.sport, schedule_number)

    @classmethod
    def detect(cls, soup):
        """
        Determine of the URL is handled by this provider.
        :param soup: The site content object to check.
        :return: Boolean of whether this site is mine.
        """
        return 'HELLO'

