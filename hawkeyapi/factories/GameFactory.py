#!/usr/bin/env python
from boto.dynamodb2.items import Item
from datetime import time
import uuid

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

        conf_status = cls.__validate_isconf(obj1, obj2, intelligent=True)
        if conf_status is None:
            ret_status = False

        opponent_status = cls.__validate_opponent(obj1, obj2)
        if opponent_status is False:
            print "OPPONENT"
            ret_status = False

        site_status = cls.__validate_site(obj1, obj2, intelligent=True)
        if site_status is False:
            print "SITE"
            ret_status = False

        start_status = cls.__validate_start(obj1, obj2, intelligent=True)
        if start_status is False:
            print "START"
            ret_status = False


    @classmethod
    def __validate_simple(cls, obj1, obj2, key):
        """
        Validate that the two values are identical.
        """
        if obj1.__dict__[key] == obj2.__dict__[key]:
            return obj1.__dict__[key]

        cls.__exception(obj1, obj2, key)
        return None

    @classmethod
    def __validate_isconf(cls, obj1, obj2, intelligent=False):
        """
        Validate that two objects agree on is_conference.
        """
        if obj1.is_conference == obj2.is_conference and obj1.is_conference is not None:
            # They are both the same so it doesnt matter
            return obj1.is_conference

        if intelligent is True:
            # Some providers dont give the status. If one is None and the
            # other is set, trust it.
            if obj1.is_conference is None and obj2.is_conference is not None:
                return obj2.is_conference
            elif obj2.is_conference is None and obj1.is_conference is not None:
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
    def __validate_site(cls, obj1, obj2, intelligent=False):
        """
        Validate that the two sites line up.
        """
        if obj1.site == 'home' and obj2.site == 'away':
            return True
        elif obj1.site == 'away' and obj2.site == 'home':
            return True
        elif obj1.site == 'neutral' and obj2.site == 'neutral':
            return True

        # In the case of an in-house scrimmage, both teams will be the same
        # as will the site
        if obj1.site == obj2.site and obj1.team_id == obj2.team_id:
            return True

        if intelligent is True:
            if obj1.site == 'UNKNOWN' and obj2.site != 'UNKNOWN':
                return True
            if obj2.site == 'UNKNOWN' and obj1.site != 'UNKNOWN':
                return True
        
        cls.__exception(obj1, obj2, "site")
        return False

    @classmethod
    def __validate_start(cls, obj1, obj2, intelligent=False):
        """
        Validate that two start times line up. If they dont see if
        we did some null value shit.
        """
        if obj1.start_time == obj2.start_time:
            return obj1.start_time

        if intelligent is True:
            # Test for 0's
            if obj1.start_time == time(0, 0, 0) or obj2.start_time == time(0, 0, 0):
                # One of them is good
                return True

            # Test for <7 minute difference for TV start
            if obj1.start_time.hour == obj2.start_time.hour:
                if abs(obj1.start_time.minute - obj2.start_time.minute) <= 7:
                    # There is a 0-7 minute difference, for TV
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
                return None
            else:
                # Its fine
                return obj2.location
        elif obj2.location is None:
            if obj1.location is None:
                return None
            else:
                # Its also fine
                return obj1.location
        elif obj1.location == obj2.location:
            return obj1.location
        else:
            cls.__exception(obj1, obj2, "location")
            return None

    @classmethod
    def __exception(cls, obj1, obj2, field):
        """
        Print an exception.
        """
        print "EXCEPTION:"
        print "  Field: %s" % field
        print "  Team 1: %s (%s)" % (obj1.__dict__[field], obj1.team_id)
        print "  Team 2: %s (%s)" % (obj2.__dict__[field], obj2.team_id)

    @classmethod
    def construct2(cls, team1, sentry1, team2, sentry2):
        """
        Return a game object from two schedule_entry objects and teams.
        """
        # Game ID
        id = uuid.uuid4()
#        # Site
#        if obj1.site == 'home' and obj2.site == 'away':
#            # 1 is the home
#            home_season = sentry1.season
#            home_league = sentry1.league
#            home_conference = team1.home_conference
#            home_team_id = team1.id
#            away_season = sentry2.season
#            away_league = sentry2.league
#            away_conference = team2.home_conference
#            away_team_id = team2.id
#        elif obj1.site == 'away' and obj2.site == 'home':
#            # 2 is the home
#            home_season = sentry2.season
#            home_league = sentry2.league
#            home_conference = team2.home_conference
#            home_team_id = team2.id
#            away_season = sentry1.season
#            away_league = sentry1.league
#            away_conference = team1.home_conference
#            away_team_id = team1.id

        # Date
        date = cls.__validate_simple(sentry1, sentry2, "date")
        # is_women
        is_women = cls.__validate_simple(sentry1, sentry2, "is_women")
        # Tournament (@TODO: implement this)
        tournament_id = None
        # Location
        location = cls.__validate_location(sentry1, sentry2)
        print location
        return

        # Return
        return Game(
            id,
            home_season,
            home_league,
            home_conference,
            home_team_id,
            away_season,
            away_league,
            away_conference,
            away_team_id,
            is_conference,
            is_women,
            is_nat_tourney,
            is_conf_tourney,
            is_tournament,
            date,
            time,
            venue,
            partial,
            links,
            tournament_id,
        )
