#!/usr/bin/env python
from boto.dynamodb2.items import Item
from datetime import time

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
        #print "** Beginning validation **"
        ret_status = True

        date_status = cls.__validate_simple(obj1, obj2, "date")
        if date_status is False:
            print "Date: '%s' vs '%s'" % (obj1.date, obj2.date)
            ret_status = False

        conf_status = cls.__validate_isconf(obj1, obj2)
        if conf_status is None:
            ret_status = False

        iswomen_status = cls.__validate_simple(obj1, obj2, "is_women")
        if iswomen_status is False:
            print "IsWomen: '%s' vs '%s'" % (obj1.is_women, obj2.is_women)
            ret_status = False

        league_status = cls.__validate_simple(obj1, obj2, "league")
        if league_status is False:
            print "League: '%s' vs '%s'" % (obj1.league, obj2.league)
            ret_status = False

        location_status = cls.__validate_location(obj1, obj2)
        if location_status is False:
            print "Location: '%s' vs '%s'" % (obj1.location, obj2.location)
            ret_status = False

        opponent_status = cls.__validate_opponent(obj1, obj2)
        if opponent_status is False:
            ret_status = False

        site_status = cls.__validate_site(obj1, obj2)
        if site_status is False:
            ret_status = False

        start_status = cls.__validate_start(obj1, obj2)
        if start_status is False:
            ret_status = False

        #print "** Finished validation **\n"
        return ret_status

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
        # @TODO: I think there are some logic issues here
        if obj1.is_conference == obj2.is_conference:
            # They are both the same so it doesnt matter
            return obj1.is_conference

        cls.__exception(obj1, obj2, "is_conference")
        return None

    @classmethod
    def __validate_opponent(cls, obj1, obj2):
        """
        Validate that the two are matching opponents.
        """
        if obj1.opponent == obj2.team_id and obj2.opponent == obj1.team_id:
            return True

        cls.__exception(obj1, obj2, "opponent")
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
        elif obj1.site == 'neutral' and obj2.site == 'neutral':
            return True
        
        cls.__exception(obj1, obj2, "site")
        return False

    @classmethod
    def __validate_start(cls, obj1, obj2):
        """
        Validate that two start times line up. If they dont see if
        we did some null value shit.
        """
        if obj1.start_time == obj2.start_time:
            return True

        cls.__exception(obj1, obj2, "start_time")
        return False

    @classmethod
    def __validate_location(cls, obj1, obj2):
        """
        Validate that two locations are the same, or if one is None.
        """
        if obj1.location is None:
            if obj2.location is None:
                return True
            else:
                # Its fine
                return True
        elif obj2.location is None:
            if obj1.location is None:
                return True
            else:
                # Its also fine
                return True

    @classmethod
    def __exception(cls, obj1, obj2, field):
        """
        Print an exception.
        """

        print "EXCEPTION:"
        print "  Field: %s" % field
        print "  Team 1: %s (%s)" % (obj1.__dict__[field], obj1.team_id)
        print "  Team 2: %s (%s)" % (obj2.__dict__[field], obj2.team_id)
