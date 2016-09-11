#!/usr/bin/env python

from datetime import time as dtime, datetime
from HawkeyApiObject import HawkeyApiObject 


class ScheduleEntry(HawkeyApiObject):
    def __init__(self, id, date, time, opponent, site, location, links,
                 conference, league, season, team_id, is_women,
                 normal_loc=None, normal_opp=None,
                 creation_date=datetime.now().replace(microsecond=0).isoformat()
                 ):
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
        self.normal_loc = normal_loc
        self.normal_opp = normal_opp
        self.creation_date = creation_date

    def __repr__(self):
        start_time = self.start_time
        if not self.start_time or self.start_time == "":
            start_time = dtime(0)
        game_time = datetime.combine(self.date, start_time).isoformat()

        team_prefix = "vs"
        location_prefix = "@"
        if self.site == "away":
            team_prefix = "at"
            location_prefix = "in"
        return "<%s %s %s %s %s %s>" % (self.__class__.__module__, game_time, team_prefix, self.opponent, location_prefix, self.location)
