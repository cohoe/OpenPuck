#!/usr/bin/env python

import datetime
from HawkeyApiObject import HawkeyApiObject 

class Game(HawkeyApiObject):
    def __init__(
        self,
        id,
        home_season,
        home_league,
        home_conference,
        home_team_id,
        away_season,
        away_league,
        away_conference,
        away_team_id,
        is_conference,
        is_women,
        is_nat_tourney,
        is_conf_tourney,
        is_tournament,
        tournament_id=None,
        date,
        time,
        venue,
        partial,
        links,
    ):
        HawkeyApiObject.__init__(self)
        self.id = id
        self.home_season = home_season
        self.home_league = home_league
        self.home_conference = home_conference
        self.home_team_id = home_team_id
        self.away_season = away_season
        self.away_league = away_league
        self.away_conference = away_conference
        self.away_team_id = away_team_id
        self.is_conference = is_conference
        self.is_women = is_women
        self.is_nat_tourney = is_nat_tourney
        self.is_conf_tourney = is_conf_tourney
        self.is_tournament = is_tournament
        self.date = date
        self.time = time
        self.venue = venue
        self.partial = partial
        self.links = links
        self.tournament_id = tournament_id


    def __repr__(self):
        start_time = self.start_time
        if not self.start_time or self.start_time == "":
            start_time = datetime.time(0)
        game_time = datetime.datetime.combine(self.date, start_time).isoformat()
        return "<%s %s %s>" % (self.__class__.__module__, game_time, self.opponent)
