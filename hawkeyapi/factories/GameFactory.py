#!/usr/bin/env python
from boto.dynamodb2.items import Item
from datetime import time
import uuid

class GameFactory():
    """
    A factory for creating and manipulating things.
    """

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
    def construct(cls, team1, sentry1, team2, sentry2):
        """
        Return a game object from two schedule_entry objects and teams.
        """
        id = uuid.uuid4()
        home_sentry, away_sentry = cls.__get_site_sentries(sentry1, sentry2)
        if home_sentry.team_id == team1.id:
            home_team = team1
            away_team = team2
        else:
            home_team = team2
            away_team = team1

        home_season = home_sentry.season
        home_league = home_sentry.league
        home_conference = home_team.home_conference
        home_team_id = home_sentry.team_id
        away_season = away_sentry.season
        away_league = away_sentry.league
        away_conference = away_team.home_conference
        away_team_id = away_sentry.team_id
        is_conference = cls.__get_isconf(home_team, home_sentry, away_team, away_sentry, True)
        is_women = cls.__get_iswomen(home_sentry, away_sentry)
        is_nat_tourney = False # @TODO: This
        is_conf_tourney = False # @TODO: This
        is_tournament = False # @TODO: This
        tournament_id = None # @TODO: This
        date = cls.__get_date(home_sentry, away_sentry)
        time = cls.__get_time(home_sentry, away_sentry, intelligent=True)
        location = cls.__get_location(home_team, home_sentry, away_team, away_sentry, intelligent=True)
        partial = cls.__get_partial(home_sentry, away_sentry)
        links = cls.__get_links(home_sentry, away_sentry)

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
            tournament_id,
            date,
            time,
            venue,
            partial,
            links,
        )

    @classmethod
    def __get_site_sentries(cls, sentry1, sentry2):
        """
        Return the correctly ordered entries for two schedule entries.
        """
        if sentry1.site == 'home':
            if sentry2.site != 'home':
                home = sentry1
                away = sentry2
            else:
                cls.__exception(sentry1, sentry2, "site")
        elif sentry1.site == 'away':
            if sentry2.site != 'away':
                home = sentry2
                away = sentry1
            else:
                cls.__exception(sentry1, sentry2, "site")
        elif sentry1.site == 'neutral':
            if sentry2.site == 'home':
                home = sentry2
                away = sentry1
            else:
                home = sentry1
                away = sentry2
        else:
            if sentry2.site == 'home':
                home = sentry2
                away = sentry1
            else:
                home = sentry1
                away = sentry2

        return home, away

    @classmethod
    def __get_isconf(cls, team1, sentry1, team2, sentry2, intelligent=False):
        """
        Return the status of if this is a conference game
        """
        if sentry1.is_conference == sentry2.is_conference and sentry1.is_conference is not None:
            return sentry1.is_conference

        if intelligent is True:
            # Some providers dont give the status. If one is None and the
            # other is set, trust it.
            if sentry1.is_conference is None and sentry2.is_conference is not None:
                return sentry2.is_conference
            elif sentry2.is_conference is None and sentry1.is_conference is not None:
                return sentry1.is_conference
            
            if team1.home_conference == team2.home_conference:
                return True
            else:
                cls.__exception(sentry1, sentry2, "is_conference")
                return None

    @classmethod
    def __get_iswomen(cls, sentry1, sentry2):
        """
        Return if this is a womens game.
        """
        return (sentry1.is_women is True or sentry2.is_women is True)

    @classmethod
    def __get_date(cls, sentry1, sentry2):
        """
        Return the date of this game.
        """
        key = "date"
        if sentry1.__dict__[key] == sentry2.__dict__[key]:
            return sentry1.__dict__[key]

        cls.__exception(sentry1, sentry2, key)
        return None

    @classmethod
    def __get_time(cls, sentry1, sentry2, intelligent=False):
        """
        Return the time of this game.
        """
        key = "start_time"
        if sentry1.__dict__[key] == sentry2.__dict__[key]:
            return sentry1.__dict__[key]

        if intelligent is True:
            # Test for 0's
            if sentry1.start_time == time(0, 0, 0) or sentry2.start_time == time(0, 0, 0):
                # One of them is good
                if sentry1.start_time ==  time(0, 0, 0):
                    return sentry2.start_time
                else:
                    return sentry1.start_time

            # Test for <7 minute difference for TV start
            if sentry1.start_time.hour == sentry2.start_time.hour:
                if abs(sentry1.start_time.minute - sentry2.start_time.minute) <= 7:
                    # There is a 0-7 minute difference, for TV
                    if sentry1.start_time.minute >= sentry2.start_time.minute:
                        return sentry1.start_time
                    else:
                        return sentry2.start_time

        cls.__exception(sentry1, sentry2, key)
        return None

    @classmethod
    def __get_location(cls, home_team, home_sentry, away_team, away_sentry, intelligent=False):
        """
        Return the normalized location of this game.
        """
        print home_sentry.location
        print away_sentry.location

    @classmethod
    def __get_partial(cls, sentry1, sentry2):
        """
        If one of our sentries is None, we have a partial game.
        """
        return (sentry1 is None or sentry2 is None)

    @classmethod
    def __get_links(cls, sentry1, sentry2):
        """
        Build a dictionary of links.
        """
        # @TODO: this might need some enhancement
        return {
            'home': sentry1.links,
            'away': sentry2.links,
        }
