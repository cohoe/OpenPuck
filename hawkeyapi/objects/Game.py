#!/usr/bin/env python

import datetime
from HawkeyApiObject import HawkeyApiObject 

class Game(HawkeyApiObject):
    def __init__(self, id, date, time, opponent, site, location, links, conference, league, season, team_id, is_women):
        HawkeyApiObject.__init__(self)

        self.team_id = team_id
        self.id = id
        self.date = date
        self.start_time = time
        self.opponent = opponent
        self.site = site
        self.location = location
        self.links = links
        self.is_conference = conference
        self.league = league
        self.season = season
        self.is_women = is_women

    def __repr__(self):
        start_time = self.start_time
        if not self.start_time or self.start_time == "":
            start_time = datetime.time(0)
        game_time = datetime.datetime.combine(self.date, start_time).isoformat()
        return "<%s %s %s>" % (self.__class__.__module__, game_time, self.opponent)
