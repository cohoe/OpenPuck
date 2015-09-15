#!/usr/bin/env python
from hawkeyapi.objects import Season

class SeasonFactory():
    """
    A factory for creating and manipulating things.
    """

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
