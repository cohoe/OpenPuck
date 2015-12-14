#!/usr/bin/env python

from hawkeyapi.database import Teams, Seasons
from hawkeyapi.factories import TeamFactory, SeasonFactory
import argparse

parser = argparse.ArgumentParser(description="Test a Provider")
parser.add_argument("--seasonids", dest="seasonids", required=True,
                    help="Comma-seperated SeasonID's (Ex: NCAA-1415-W")
parser.add_argument("--teamids", dest="teamids", required=True,
                    help="Comma-seperated TeamID (Ex: NCAA-RIT-W")
args = parser.parse_args()

for season_id in args.seasonids.split(','):
    season_item = Seasons.get_item(id=season_id)
    season_obj = SeasonFactory.objectify(season_item)

    for team_id in args.teamids.split(','):
        team_item = Teams.get_item(id=team_id)
        team_obj = TeamFactory.objectify(team_item)

        print team_obj.json()

        sentry_objs = team_obj.get_provider().get_schedule(season_obj)

        for sentry_obj in sentry_objs:
            print sentry_obj.json()
            #print "%ss" % (sentry_obj.opponent, sentry_obj.is_conference)
