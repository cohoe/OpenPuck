#!/usr/bin/env python

from hawkeyapi.database import Teams, Seasons
from hawkeyapi.factories import TeamFactory, SeasonFactory

season_item = Seasons.get_item(id='NCAA-1415-W')
season_obj = SeasonFactory.objectify(season_item)

team_item = Teams.get_item(id='NCAA-BU-W')
team_obj = TeamFactory.objectify(team_item)

print team_obj.json()

sentry_objs = team_obj.get_provider().get_schedule(season_obj)

for sentry_obj in sentry_objs:
    #print sentry_obj.json()
    print "%s - %s" % (sentry_obj.opponent, sentry_obj.is_conference)
