#!/usr/bin/env python

from hawkeyapi.database import ScheduleEntries, Teams
from hawkeyapi.objects import ScheduleEntry, Team
from hawkeyapi.util import get_uncombined_timestamp
from hawkeyapi.TestData import seasons
from boto.dynamodb2.exceptions import ItemNotFound

season = seasons[1]

#team = Teams.get_item(id='NCAA-Yale-W')
team_id = 'NCAA-RIT-W'
t_entry = Teams.get_item(id=team_id)

entries = ScheduleEntries.query_2(
    team_id__eq=team_id
)

for e_db in entries:
    e_myid = e_db['id']
    [date, time] = get_uncombined_timestamp(e_db['timestamp'])
    e_obj = ScheduleEntry(
        e_db['entry_id'],
        date,
        time,
        e_db['opponent'],
        e_db['site'],
        e_db['location'],
        e_db['links'],
        e_db['is_conference'],
        season
    )

    try:
        opponent_entry = Teams.scan(altnames__contains=e_obj.opponent, is_women__eq=t_entry['is_women'])
        results_list = list(opponent_entry)
        num_results = len(results_list)
        if num_results == 0:
            raise ItemNotFound
        elif num_results > 1:
            raise Exception("Too many results (%i) for %s?" % (num_results, e_obj.opponent))
        o_entry = results_list[0]
        print "Found opponent %s" % o_entry['id']
    except ItemNotFound:
        print "Could not find %s" % e_obj.opponent
    except Exception as e:
        print "Failed to find %s" % e_obj.opponent
        print e
