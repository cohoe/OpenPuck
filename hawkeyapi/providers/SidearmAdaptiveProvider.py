#!/usr/bin/env python

from Provider import *


class SidearmAdaptiveProvider(Provider):
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
        }

    def get_schedule(self):
        """
        Return a list of JSON objects of the schedule.
        """
        html = self.get_schedule_from_web()
        soup = BeautifulSoup(html)

        json_games = []

        # Some schedules dont even put the year...
        schedule_years = self.get_schedule_years(soup)

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
            # @TODO: Deal with dashes in the datestamp again
            date_string, date_format = self.get_game_date(game, schedule_years)
            time_string, time_format = self.get_game_time(game)
            if "-" in date_string:
                print "LOLNOPE"
                continue

            timestamp = get_combined_timestamp(date_string, date_format, time_string, time_format)
            print timestamp.isoformat()

            json_game = self.get_json_entry(game_id, timestamp, opponent, site, location, links)
            json_games.append(json_game)

        return json_games

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

        opponent_element = game.find('div', class_='schedule_game_opponent_name')
        opponent = opponent_element.text

        return self.get_normalized_opponent(opponent)

    def get_schedule_years(self, soup):
        """
        Return two integers representing the years of this schedule.
        """
        page_title = soup.find('div', class_='page_title').text
        year_string = re.sub(r'[^\d-]', '', page_title)
        years = year_string.split("-")
        n_years = []
        for year in years:
            if len(year) < 4:
                year = "20" + year
            n_years.append(int(year))
        return n_years

    def get_game_media_urls(self, game):
        """
        Return a normalized dictionary of media URLs.
        """
        media_urls = {
            'video': False,
            'audio': False,
            'stats': False,
        }

        media_element = game.find('div', class_='schedule_game_multimedia_links')
        if not media_element:
            return media_urls

        link_elements = media_element.find_all('a', class_='schedule_game_media_link')
        for link in link_elements:
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
        Returns the raw game date and format.
        """
        date_string = game.find('div', class_='schedule_game_opponent_date').text.upper().strip()
        if re.search(r'[a-zA-Z]', date_string):
            if re.search(r'SEPT|OCT|NOV|DEC', date_string):
                date_string = date_string + " %i" % years[0]
            else:
                date_string = date_string + " %i" % years[1]
            date_format = "%a, %B %d %Y"
        elif "." in date_string:
            date_format = "%m.%d.%y"
        elif "/" in date_string:
            date_format = "%m/%d/%Y"

        return date_string, date_format

    def get_game_time(self, game):
        """
        Return the raw gate time and format.
        """
        time_string = game.find('div', class_='schedule_game_opponent_time').text.strip()
        time_string = time_string.upper().replace('.', '')

        # If there are any word times
        if "TBA" in time_string or time_string == "":
            time_string = "12:00 AM"
        if "NOON" in time_string:
            time_string = "12:00 PM"

        # Figure out the time format to use
        if " " in time_string:
            if ":" in time_string:
                time_format = "%I:%M %p"
            else:
                time_format = "%I %p"
        else:
            if ":" in time_string:
                time_format = "%I:%M%p"
            else:
                time_format = "%I%p"

        return time_string, time_format
