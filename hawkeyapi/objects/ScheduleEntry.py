#!/usr/bin/env python

from HawkeyApiObject import HawkeyApiObject 
from hawkeyapi.CommonDates import *
from datetime import time

class ScheduleEntry(HawkeyApiObject):
    def __init__(self, id, timestamp, opponent, site, location, links, conference, schedule_years):
        HawkeyApiObject.__init__(self)

        self.id = id
        self.date = timestamp.date()
        self.start_time = self.__get_starttime(timestamp.time())
        self.opponent = opponent
        self.site = site
        self.location = location
        self.is_conference_tournament = self.__is_conf_tournament(timestamp)
        self.is_national_tournament = self.__is_national_tournament(timestamp)
        self.links = links
        self.is_conference = conference
        self.season = schedule_years

    def __repr__(self):
        return "<%s %s %s>" % (self.__class__.__module__, self.date, self.opponent)

    def __is_conf_tournament(self, timestamp):
        return (timestamp >= DATE_CONFERENCE_TOURNAMENT_START and
                timestamp < DATE_NATIONAL_TOURNAMENT_START)

    def __is_national_tournament(self, timestamp):
        return (timestamp >= DATE_NATIONAL_TOURNAMENT_START)

    def __get_starttime(self, starttime):
        if starttime != time(0):
            return starttime
