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
        print "** Beginning validation **"

        date_status = cls.__validate_simple(obj1, obj2, "date")
        if date_status is False:
            print "Date: '%s' vs '%s'" % (obj1.date, obj2.date)

        conf_status = cls.__validate_isconf(obj1, obj2)
        if conf_status is None:
            print "IsConference: '%s' vs '%s'" % (obj1.is_conference, obj2.is_conference)

        iswomen_status = cls.__validate_simple(obj1, obj2, "is_women")
        if iswomen_status is False:
            print "IsWomen: '%s' vs '%s'" % (obj1.is_women, obj2.is_women)

        league_status = cls.__validate_simple(obj1, obj2, "league")
        if league_status is False:
            print "League: '%s' vs '%s'" % (obj1.league, obj2.league)

        location_status = cls.__validate_location(obj1, obj2)
        if location_status is False:
            print "Location: '%s' vs '%s'" % (obj1.location, obj2.location)

        opponent_status = cls.__validate_opponent(obj1, obj2)
        if opponent_status is False:
            print "Opponent: '%s' vs '%s'" % (obj1.opponent, obj2.opponent)

        site_status = cls.__validate_site(obj1, obj2)
        if site_status is False:
            print "Site: '%s' vs '%s'" % (obj1.site, obj2.site)

        start_status = cls.__validate_start(obj1, obj2)
        if start_status is False:
            print "Start: '%s' vs '%s'" % (obj1.start_time, obj2.start_time)

        print "** Finished validation **\n"

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

        else:
            # Something is missing. If one is none then we'll trust the other
            if obj1.is_conference is None:
                return obj2.is_conference
            elif obj2.is_conference is None:
                return obj1.is_conference
            else:
                return None

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

    @classmethod
    def __validate_start(cls, obj1, obj2):
        """
        Validate that two start times line up. If they dont see if
        we did some null value shit.
        """
        if obj1.start_time == time(0, 0, 0):
            if obj2.start_time == time(0, 0, 0):
                return True
            else:
                # They are different but the first obj has no start, so too bad
                return True
        elif obj1.start_time == obj2.start_time:
            return True

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
