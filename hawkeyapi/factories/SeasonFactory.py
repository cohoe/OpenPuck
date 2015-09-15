#!/usr/bin/env python
from hawkeyapi.objects import Season
from boto.dynamodb2.items import Item

class SeasonFactory():
    """
    A factory for creating and manipulating things.
    """

    @classmethod
    def objectify(cls, e_db):
        """
        Turn an item into an object.
        """
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

    @classmethod
    def itemify(cls, db_table, obj):
        """
        Turn an object into an item.
        """
        return Item(
            db_table,
            data = {
                'league': obj.league,
                'id': obj.id,
                'is_women': obj.is_women,
                'start': obj.start_year,
                'end': obj.end_year,
                'confplay': list(obj.phases['ConferencePlay']),
                'conftour': list(obj.phases['ConferenceTournament']),
                'nattour': list(obj.phases['NationalTournament']),
            },
        )
