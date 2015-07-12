#!/usr/bin/env python

from bs4 import BeautifulSoup
from datetime import datetime
from hawkeyapi.CommonLib import *
from hawkeyapi.CommonDates import *

# @TODO: Stats, Audio, Video links

def parse_schedule_to_json(url, html):
#    soup = BeautifulSoup(html, 'html.parser')
#
#    # Get the table to schedule entries
    schedule_table = soup('table', 'default_dgrd')[0]

    json_games = []

    for child in schedule_table.children:
        child_soup = BeautifulSoup(unicode(child))
        cells = child_soup.find_all('td')

        if cells:
            # Get the game ID
            game_id = int(child["id"].split("_")[-1])

            # Clean up the data that we use
            opponent = chomp(cells[2].text)
            date_string = chomp(cells[0].text)
            time_string = chomp(cells[5].text)
            location = chomp(cells[3].text)

            # Some of the data comes in cleanly
            raw_site = cells[4].text

            # Get any media URLs
            links = get_game_media_urls(get_base_from_url(url), game_id)

            # Check if we have a range of dates for a given schedule entry
            if "-" in date_string:
                month, days, year = date_string.split('/')
                start_day, end_day = days.split('-')

                start_day = int(start_day)
                end_day = int(end_day)
                month = int(month)
                year = int(year)

                end_day += 1

                for day in range(start_day, end_day):
                    date_string = "%i/%i/%i" % (month, day, year)
                    json = make_normalized_game(game_id, opponent, date_string, time_string, raw_site, location, links)
            else:
                json = make_normalized_game(game_id, opponent, date_string, time_string, raw_site, location, links)

            json_games.append(json)

    return json_games


def make_normalized_game(game_id, opponent, date_string, time_string, raw_site, location, links):
#    # Determine site
#    if raw_site.upper() == "H":
#        site = "home"
#    elif raw_site.upper() == "A":
#        site = "away"
#    elif raw_site.upper() == "N":
#        site = "neutral"
#    else:
#        site = "UNKNOWN (ERR)"

    # Deal with the time
#    game_time = get_timestamp_from_parts(date_string, time_string)

#    # Is this a conference tournament game?
#    is_conf_tournament = False
#    if game_time >= DATE_CONFERENCE_TOURNAMENT_START and game_time < DATE_NATIONAL_TOURNAMENT_START:
#        is_conf_tournament = True
#
#    # Is this a national tournament game?
#    is_national_tournament = False
#    if game_time >= DATE_NATIONAL_TOURNAMENT_START:
#        is_national_tournament = True
#
#    # Is this a pre-season game?
#    is_preseason = False
#    if game_time < DATE_SEASON_START:
#        is_preseason = True;

    # Get the location of the game
#    location = normalize_location(location)


    # Now take all of this data and mash it together into a single object
    raw_game_for_json = {}
    raw_game_for_json['gameId'] = game_id
    raw_game_for_json['startTime'] = game_time.isoformat()
    raw_game_for_json['opponent'] = opponent
    raw_game_for_json['site'] = site
    raw_game_for_json['isConfTourney'] = is_conf_tournament
    raw_game_for_json['isNatTourney'] = is_national_tournament
    raw_game_for_json['isPreSeason'] = is_preseason
    raw_game_for_json['location'] = location
    raw_game_for_json['mediaUrls'] = links
    raw_game_for_json['provider'] = "SidearmLegacy"

    return dict2json("raw_game", raw_game_for_json, True)

#def get_timestamp_from_parts(date_string, time_string):
#    """
#    Return a datetime object representing the start time of a game.
#    """
#
#    date_format = "%m/%d/%Y"
#    date_obj = datetime.strptime(date_string, date_format)
#
#    # Schedules often give a TBA. Set this to midnight since no game
#    # will actually start at midnight.
#    if "TBA" in time_string:
#        time_obj = datetime.strptime("12:00 AM", "%I:%M %p")
#    else:
#        time_string = time_string.upper().replace('.', '')
#        if ":" in time_string:
#            time_format = "%I:%M %p"
#        else:
#            time_format = "%I %p"
#        time_obj = datetime.strptime(time_string, time_format)
#
#    return datetime.combine(date_obj, time_obj.time())


#def get_game_media_urls(server, game_id):
#    """
#    Get the extras box for a given game
#    """
#    media_urls = {}
#    media_urls['video'] = False
#    media_urls['audio'] = False
#    media_urls['stats'] = False
#
#    url = server + "/services/schedule_detail.aspx?id=%i" % game_id
#    contents = get_html_from_url(url)
#    soup = BeautifulSoup(contents)
#
#    stats_string = soup.find(text="Live Stats")
#    if stats_string:
#        stats_url = stats_string.parent['href']
#        media_urls['stats'] = stats_url
#
#
#    return media_urls
