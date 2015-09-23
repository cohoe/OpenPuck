#!/usr/bin/env python
from hawkeyapi.objects import SeasonPhase
from boto.dynamodb2.items import Item
from datetime import date

class SeasonPhaseFactory():
    """
    A factory for creating and manipulating things.
    """

    @classmethod
    def objectify(cls, e_db):
        """
        Turn an item into an object.
        """
        return SeasonPhase(
            e_db['id'],
            e_db['name'],
            date.fromordinal(int(e_db['start'])),
            date.fromordinal(int(e_db['end'])),
        )

    @classmethod
    def itemify(cls, db_table, obj):
        """
        Turn an object into an item.
        """
        return Item(
            db_table,
            data = {
                'id': obj.id,
                'name': obj.name,
                'start': date.toordinal(obj.start),
                'end': date.toordinal(obj.end),
            },
        )
