#!/usr/bin/env python
from hawkeyapi.objects import Team
from boto.dynamodb2.items import Item

class TeamFactory():
    """
    A factory for creating and manipulating things.
    """

    @classmethod
    def objectify(cls, e_db):
        """
        Turn an item into an object.
        """
        return Team(
            e_db['id'],
            e_db['institution'],
            e_db['mascot'],
            bool(e_db['is_women']),
            e_db['home_conference'],
            e_db['social_media'],
            e_db['website'],
            e_db['provider'],
            e_db['league'],
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
                'institution': obj.institution_name,
                'mascot': obj.mascot,
                'is_women': obj.is_women,
                'home_conference': obj.home_conference,
                'provider': obj.provider,
                'league': obj.league,
                'website': obj.website,
                'social_media': obj.social_media,
            },
        )
