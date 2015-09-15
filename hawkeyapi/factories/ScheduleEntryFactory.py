#!/usr/bin/env python
from hawkeyapi.objects import ScheduleEntry
from boto.dynamodb2.items import Item
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
            dateparser.parse(e_db['date']).date(),
            dateparser.parse(e_db['start_time']).time(),
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
        """
        Turn an object into an item.
        """
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
