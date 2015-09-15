#!/usr/bin/env python

from hawkeyapi.database import ScheduleEntries, Teams, TeamAltnames, Seasons
from hawkeyapi.factories import ScheduleEntryFactory, SeasonFactory
from boto.dynamodb2.exceptions import ItemNotFound
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("team_id", metavar='team_id')
args = parser.parse_args()

s_db = Seasons.get_item(league='NCAA', id='2014-15W')
season = SeasonFactory.objectify(s_db)

#team = Teams.get_item(id='NCAA-Yale-W')
#team_id = 'NCAA-Harvard-W'
team_id = args.team_id
print "Searching for %s" % team_id
t_entry = Teams.get_item(id=team_id)

entries = ScheduleEntries.query_2(
    team_id__eq=team_id
)

for e_db in entries:
    e_myid = e_db['id']
    e_obj = ScheduleEntryFactory.objectify(e_db)

    try:
        opponent_entry = TeamAltnames.query(index='AltnamesGenderIndex', altname__eq=e_obj.opponent, is_women__eq=t_entry['is_women'])
        results_list = list(opponent_entry)
        num_results = len(results_list)
        if num_results == 0:
            raise ItemNotFound
        elif num_results > 1:
            raise Exception("Too many results (%i) for %s?" % (num_results, e_obj.opponent))
        o_entry = results_list[0]
        print "Found opponent %s" % o_entry['team_id']
    except ItemNotFound:
        print "Could not find %s" % e_obj.opponent
    except Exception as e:
        print "Failed to find %s" % e_obj.opponent
        print e
