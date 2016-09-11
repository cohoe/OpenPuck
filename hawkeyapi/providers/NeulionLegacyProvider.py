#!/usr/bin/env python

from Provider import *


class NeulionLegacyProvider(Provider):
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
        soup = get_soup_from_content(get_html_from_url(index_url))

        # @TODO: There has to be a better way to do this....
        sched_opts = ["Schedules/Results", "Schedule & Results",
                      "Schedule/Results", "Schedule"]
        sched_element = soup.find(id='section-menu').find('a', text=sched_opts)
        self.urls = {
            'index': index_url,
            'schedule': self.server + sched_element['href']
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
            # Location
            location = self.get_game_location(game)
            # Site
            site = self.get_game_site(game)
            # Opponent
            opponent = self.get_game_opponent(game)
            # Links
            links = self.get_game_media_urls(game)
            # Timestamp
            game_date = self.get_game_date(game, self.season.years())
            game_time = self.get_game_time(game)
            # Game ID
            game_id = self.get_gameid_from_date_time(game_date, game_time)
            # Conference
            conference = self.get_game_conference(game)

            game = ScheduleEntry(game_id, game_date, game_time, opponent, site,
                                 location, links, conference,
                                 self.season.league, self.season.id,
                                 self.team_id, self.is_women)
            games.append(game)

        return games

    @classmethod
    def get_game_entries(cls, soup):
        """
        Return a list of elements containing games. Usually divs or rows.
        """
        schedule_table = soup.find(id="schedule-table")
        headers = [header.text.upper().strip() for header in
                   schedule_table.find_all('th')]
        headers.append("SITE")
        results = []
        for row in schedule_table.find_all('tr'):
            game = {}
            for i, cell in enumerate(row.find_all('td')):
                game[headers[i]] = cell
            game["SITE"] = row.attrs['class']
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
        if "home" in game['SITE']:
            return self.get_normalized_site("home")
        elif "sm" in game['SITE']:
            return self.get_normalized_site("unknown")
        else:
            return self.get_normalized_site("away")

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

        video_element = game['WATCH']
        if video_element.find('a', href=True) is not None:
            media_urls['video'] = video_element.find('a', href=True)['href']

        link_element = game['RELATED LINKS']
        for link in link_element.find_all('a', href=True):
            if link.get('title') == "Live Stats":
                if 'http' not in link['href']:
                    media_urls['stats'] = self.server + link['href']
                else:
                    media_urls['stats'] = link['href']

        return media_urls

    @classmethod
    def get_game_time(cls, game):
        """
        Return a time object of the games start time.
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

        return get_time_from_string(time_string)

    @classmethod
    def get_game_date(cls, game, years):
        """
        Return a date object of the games start date.
        """
        date_string = game['DATE'].text.strip().upper()

        return get_date_from_string(date_string, years)

    @classmethod
    def get_game_conference(cls, game):
        """
        Is this a conference game?
        """
        raw_opponent = game['OPPONENT'].text.strip()
        return "*" in raw_opponent

    def get_schedule_url_for_season(self, season):
        """
        Return the full URL of the schedule for a given season.
        """
        return "%s&Q_SEASON=%i" % (self.urls['schedule'], season.start_year)

    @classmethod
    def detect(cls, soup):
        """
        Determine of the URL is handled by this provider.
        :param soup: The site content object to check.
        :return: Boolean of whether this site is mine.
        """
        if soup.body.get('class') is not None:
            if 'desktop' in soup.body.get(
                    'class') and 'sport-home' in soup.body.get('class'):
                return True

        return False
