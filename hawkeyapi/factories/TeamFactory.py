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
            e_db['institution'],
            e_db['mascot'],
            bool(e_db['is_women']),
            e_db['home_conference'],
            e_db['social_media'],
            e_db['web_site'],
            e_db['provider'],
            e_db['league'],
        )

    @classmethod
    def itemify(cls, db_table, team_id, obj):
        """
        Turn an object into an item.
        """
        #@TODO: Add team_id
        return Item(
            db_table,
            data = {
                'id': team_id,
                'institution': obj.institution_name,
                'mascot': obj.mascot,
                'is_women': obj.is_women,
                'home_conference': obj.home_conference,
                'provider': obj.provider,
                'league': obj.league,
                'web_site': obj.website,
                'social_media': obj.social_media,
            },
        )
