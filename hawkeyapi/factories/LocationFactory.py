#!/usr/bin/env python
from hawkeyapi.objects import Location
from boto.dynamodb2.items import Item

class LocationFactory():
    """
    A factory for creating and manipulating things.
    """

    @classmethod
    def objectify(cls, e_db):
        """
        Turn an item into an object.
        """
        return Location(
            e_db['id'],
            e_db['cn'],
            e_db['street'],
            e_db['city'],
            e_db['state'],
            e_db['postal'],
            e_db['country'],
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
                'cn': obj.cn,
                'street': obj.street,
                'city': obj.city,
                'state': obj.state,
                'postal': obj.postal,
                'country': obj.country,
            },
        )
