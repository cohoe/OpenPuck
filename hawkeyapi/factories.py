#!/usr/bin/env python

from hawkeyapi.objects import Team, ScheduleEntry, Season
from hawkeyapi.util import *
from boto.dynamodb2.items import Item
from dateutil import parser as dateparser

class TeamFactory():
    @classmethod
    def objectify(cls, e_db):
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
    def objectify(cls, e_db):
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
    def objectify(cls, e_db):
        return ScheduleEntry(
            e_db['entry_id'],
            dateparser.parse(e_db['date']).date(),
            dateparser.parse(e_db['time']).time(),
            e_db['opponent'],
            e_db['site'],
            e_db['location'],
            e_db['links'],
            bool(e_db['is_conference']),
            e_db['league'],
            e_db['season'],
        )

    @classmethod
    def itemify(cls, db_table, team_id, obj):
        return Item(
            db_table,
            data = {
                'team_id': team_id,
                'entry_id': obj.id,
                'date': obj.date.isoformat(),
                'start_time': obj.start_time.isoformat(),
                'opponent': obj.opponent,
                'site': obj.site,
                'location': obj.location,
                'links': obj.links,
                'is_conference': obj.is_conference,
                'season': obj.season,
                'league': obj.league,
            },
        )
