#!/usr/bin/env python

from hawkeyapi.objects import Team, ScheduleEntry, Season
from hawkeyapi.util import *

class TeamFactory():
    @classmethod
    def make(cls, e_db):
        return Team(
            e_db['institution'],
            e_db['mascot'],
            bool(e_db['is_women']),
            e_db['home_conference'],
            e_db['social_media'],
            e_db['web_site'],
            e_db['provider'],
            e_db['league'],
        )

class SeasonFactory():
    @classmethod
    def make(cls, e_db):
        return Season(
            e_db['league'],
            e_db['id'],
            bool(e_db['is_women']),
            int(e_db['start']),
            int(e_db['end']),
            tuple(e_db['confplay']),
            tuple(e_db['conftour']),
            tuple(e_db['nattour']),
        )

class ScheduleEntryFactory():
    @classmethod
    def make(cls, e_db):
        return ScheduleEntry(
            e_db['entry_id'],
            e_db['date'],
            e_db['time'],
            e_db['opponent'],
            e_db['site'],
            e_db['location'],
            e_db['links'],
            bool(e_db['is_conference']),
            e_db['league'],
            e_db['season'],
        )
