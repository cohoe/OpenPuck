#!/usr/bin/env python
from boto.dynamodb2.items import Item

class GameFactory():
    """
    A factory for creating and manipulating things.
    """

    @classmethod
    def objectify(cls, e_db):
        """
        Turn an item into an object.
        """
        pass

    @classmethod
    def itemify(cls, db_table, obj):
        """
        Turn an object into an item.
        """
        pass

    @classmethod
    def construct(cls, obj1, obj2, override=False):
        """
        Make a game object from two ScheduleEntries
        """
        print "** Beginning validation **"

        date_status = cls.__validate_simple(obj1, obj2, "date")
        print "Date: %s" % date_status

        conf_status = cls.__validate_isconf(obj1, obj2)
        print "IsConference: %s" % conf_status

        iswomen_status = cls.__validate_simple(obj1, obj2, "is_women")
        print "IsWomen: %s" % iswomen_status

        league_status = cls.__validate_simple(obj1, obj2, "league")
        print "League: %s" % league_status

        location_status = cls.__validate_simple(obj1, obj2, "location")
        print "Location: %s" % location_status

        opponent_status = cls.__validate_opponent(obj1, obj2)
        print "Opponent: %s" % opponent_status

        site_status = cls.__validate_site(obj1, obj2)
        print "Site: %s" % site_status

        start_status = cls.__validate_simple(obj1, obj2, "start_time")
        print "StartTime: %s" % start_status

        print "** Finished validation **"

    @classmethod
    def __validate_simple(cls, obj1, obj2, key):
        """
        Validate that the two values are identical.
        """
        return (obj1.__dict__[key] == obj2.__dict__[key])

    @classmethod
    def __validate_isconf(cls, obj1, obj2):
        """
        Validate that two objects agree on is_conference.
        """
        if obj1.is_conference == obj2.is_conference:
            # They are both the same so it doesnt matter
            return obj1.is_conference

        else:
            # Something is missing. If one is none then we'll trust the other
            if obj1.is_conference is None:
                return obj2.is_conference
            elif obj2.is_conference is None:
                return obj1.is_conference
            else:
                return False

    @classmethod
    def __validate_opponent(cls, obj1, obj2):
        """
        Validate that the two are matching opponents.
        """
        if obj1.opponent == obj2.team_id and obj2.opponent == obj1.team_id:
            return True

        return False

    @classmethod
    def __validate_site(cls, obj1, obj2):
        """
        Validate that the two sites line up.
        """
        if obj1.site == 'home' and obj2.site == 'away':
            return True
        elif obj1.site == 'away' and obj2.site == 'home':
            return True
        
        return False
