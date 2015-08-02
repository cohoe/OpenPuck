#!/usr/bin/env python

import datetime
from HawkeyApiObject import HawkeyApiObject 
from hawkeyapi.CommonDates import *

class ScheduleEntry(HawkeyApiObject):
    def __init__(self, id, date, time, opponent, site, location, links, conference, season):
        HawkeyApiObject.__init__(self)

        self.id = id
        self.date = date
        self.start_time = time
        self.opponent = opponent
        self.site = site
        self.location = location
        self.is_conference_tournament = self.__is_conf_tournament(date)
        self.is_national_tournament = self.__is_national_tournament(date)
        self.links = links
        self.is_conference = conference
        self.season = season.id
        self.league = season.league

    def __repr__(self):
        start_time = self.start_time
        if not self.start_time or self.start_time == "":
            start_time = datetime.time(0)
        game_time = datetime.datetime.combine(self.date, start_time).isoformat()
        return "<%s %s %s>" % (self.__class__.__module__, game_time, self.opponent)

    def __is_conf_tournament(self, date):
        return (date >= DATE_CONFERENCE_TOURNAMENT_START and
                date < DATE_NATIONAL_TOURNAMENT_START)

    def __is_national_tournament(self, date):
        return (date >= DATE_NATIONAL_TOURNAMENT_START)
