#!/usr/bin/env python
from hawkeyapi.objects import ScheduleEntry
from boto.dynamodb2.items import Item
from datetime import date
from dateutil import parser as dateparser

class ScheduleEntryFactory():
    """
    A factory for creating and manipulating things.
    """

    @classmethod
    def objectify(cls, e_db):
        """
        Turn an item into an object.
        """
        return ScheduleEntry(
            e_db['entry_id'],
            date.fromordinal(e_db['date']),
            dateparser.parse(e_db['start_time']).time(),
            e_db['opponent'],
            e_db['site'],
            e_db['location'],
            e_db['links'],
            bool(e_db['is_conference']),
            e_db['league'],
            e_db['season'],
            e_db['team_id'],
        )

    @classmethod
    def itemify(cls, db_table, obj):
        """
        Turn an object into an item.
        """
        return Item(
            db_table,
            data = {
                'team_id': obj.team_id,
                'entry_id': obj.id,
                'date': obj.date.toordinal(),
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
