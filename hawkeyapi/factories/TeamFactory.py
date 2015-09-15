#!/usr/bin/env python
from hawkeyapi.objects import Team

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

