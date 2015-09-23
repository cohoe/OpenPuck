#!/usr/bin/env python

from hawkeyapi.database import ScheduleEntries, Teams, TeamAltnames, Seasons
from hawkeyapi.factories import ScheduleEntryFactory, SeasonFactory, GameFactory
from boto.dynamodb2.exceptions import ItemNotFound

s_db = Seasons.get_item(id='NCAA-1415-W')
season = SeasonFactory.objectify(s_db)

#team = Teams.get_item(id='NCAA-Yale-W')
team_id = 'NCAA-Harvard-W'
print "Searching for %s" % team_id
t_entry = Teams.get_item(id=team_id)

print "Finding schedule entries..."
entries = ScheduleEntries.query_2(
    index='TeamSeasonIndex',
    team_id__eq=team_id,
    season__eq=season.id,
)

# For schedule_entries for the given team...
for e_db in entries:
    # Make an object for it
    e_obj = ScheduleEntryFactory.objectify(e_db)

    try:
        # Find the item for the opponent
        opponent_entry = Teams.get_item(id=e_obj.opponent)
        o_entry = opponent_entry
        print "Found opponent %s" % o_entry['id']
        try:
            opponent_s_entry = ScheduleEntries.get_item(team_id=o_entry['id'], date=e_obj.date.toordinal())
            print "Their opponent is: %s" % opponent_s_entry['opponent']
            # WE HAVE REACHED SUCCESS!!!!
            my_obj = e_obj
            their_obj = ScheduleEntryFactory.objectify(opponent_s_entry)
            g_obj = GameFactory.construct(my_obj, their_obj)
        except Exception as e:
            print "Could not find matching entry (%s)" % e
            #pass
    except ItemNotFound:
        print "Could not find %s" % e_obj.opponent
    except Exception as e:
        print "Failed to find %s" % e_obj.opponent
        print e
